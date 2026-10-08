"""One-process-at-a-time paced file replay with an in-memory MJPEG frame buffer.

FFmpeg is an external runtime executable. The adapter does not download or
install it and never accepts a path from an HTTP request; it receives only a
catalog-resolved DemoClip from the controller.
"""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import threading
from typing import Callable

from app.demo.clip_catalog import DemoClip
from app.demo.controller import PlaybackCallbacks


MAX_JPEG_FRAME_BYTES = 16 * 1024 * 1024


class FFmpegReplayAdapter:
    def __init__(
        self,
        ffmpeg_binary: str,
        *,
        process_factory: Callable[..., subprocess.Popen] = subprocess.Popen,
        join_timeout_seconds: float = 2.0,
    ) -> None:
        self._ffmpeg_binary = ffmpeg_binary
        self._process_factory = process_factory
        self._join_timeout_seconds = join_timeout_seconds
        self._lock = threading.RLock()
        self._frame_condition = threading.Condition(self._lock)
        self._stop_event = threading.Event()
        self._restart_event = threading.Event()
        self._worker: threading.Thread | None = None
        self._process: subprocess.Popen | None = None
        self._clip: DemoClip | None = None
        self._callbacks: PlaybackCallbacks | None = None
        self._latest_frame: bytes | None = None
        self._frame_sequence = 0

    @classmethod
    def from_environment(cls) -> "FFmpegReplayAdapter | None":
        configured = os.environ.get("SENTINEL_FFMPEG_BINARY", "ffmpeg").strip()
        if not configured:
            return None
        resolved = shutil.which(configured)
        if resolved is None and Path(configured).is_file():
            resolved = str(Path(configured).resolve())
        return cls(resolved) if resolved else None

    def start(self, clip: DemoClip, callbacks: PlaybackCallbacks) -> None:
        with self._lock:
            if self._worker is not None and self._worker.is_alive():
                raise RuntimeError("A replay worker is already active.")
            self._stop_event.clear()
            self._restart_event.clear()
            self._clip = clip
            self._callbacks = callbacks
            self._latest_frame = None
            self._worker = threading.Thread(
                target=self._run,
                name="sentinel-demo-replay",
                daemon=True,
            )
            self._worker.start()

    def stop(self) -> None:
        self._stop_event.set()
        self._restart_event.clear()
        self._terminate_process()
        with self._frame_condition:
            self._latest_frame = None
            self._frame_condition.notify_all()
            worker = self._worker
        if worker is not None and worker is not threading.current_thread():
            worker.join(self._join_timeout_seconds)
            if worker.is_alive():
                self._kill_process()
                worker.join(self._join_timeout_seconds)
            if worker.is_alive():
                raise RuntimeError("Replay worker did not stop within the cleanup limit.")

    def restart(self, callbacks: PlaybackCallbacks) -> None:
        with self._frame_condition:
            if self._worker is None or not self._worker.is_alive():
                raise RuntimeError("Replay worker is not active.")
            self._callbacks = callbacks
            self._latest_frame = None
            self._restart_event.set()
            self._frame_condition.notify_all()
        self._terminate_process()

    def wait_for_frame(
        self, after_sequence: int, timeout_seconds: float = 1.0
    ) -> tuple[int, bytes] | None:
        with self._frame_condition:
            self._frame_condition.wait_for(
                lambda: self._frame_sequence > after_sequence
                or self._stop_event.is_set(),
                timeout=timeout_seconds,
            )
            if self._frame_sequence > after_sequence and self._latest_frame is not None:
                return self._frame_sequence, self._latest_frame
            return None

    @staticmethod
    def _extract_jpeg_frames(buffer: bytearray) -> list[bytes]:
        frames: list[bytes] = []
        while True:
            start = buffer.find(b"\xff\xd8")
            if start < 0:
                if len(buffer) > 1:
                    del buffer[:-1]
                break
            if start:
                del buffer[:start]
            end = buffer.find(b"\xff\xd9", 2)
            if end < 0:
                if len(buffer) > MAX_JPEG_FRAME_BYTES:
                    raise ValueError("Decoded frame exceeds the configured size limit.")
                break
            end += 2
            if end > MAX_JPEG_FRAME_BYTES:
                raise ValueError("Decoded frame exceeds the configured size limit.")
            frames.append(bytes(buffer[:end]))
            del buffer[:end]
        return frames

    def _build_command(self, clip: DemoClip) -> list[str]:
        return [
            self._ffmpeg_binary,
            "-hide_banner",
            "-loglevel",
            "error",
            "-nostdin",
            "-re",
            "-i",
            str(clip.resolved_path),
            "-map",
            "0:v:0",
            "-an",
            "-progress",
            "pipe:2",
            "-stats_period",
            "0.25",
            "-f",
            "image2pipe",
            "-vcodec",
            "mjpeg",
            "-q:v",
            "5",
            "pipe:1",
        ]

    def _run(self) -> None:
        loop_pending = False
        first_process = True
        while not self._stop_event.is_set():
            with self._lock:
                clip = self._clip
                callbacks = self._callbacks
            if clip is None or callbacks is None:
                return

            try:
                process = self._process_factory(
                    self._build_command(clip),
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    bufsize=0,
                )
            except (OSError, ValueError):
                callbacks.failed()
                return

            with self._lock:
                self._process = process

            progress_thread = threading.Thread(
                target=self._read_progress,
                args=(process, callbacks),
                name="sentinel-demo-progress",
                daemon=True,
            )
            progress_thread.start()
            frame_buffer = bytearray()
            frames_this_pass = 0
            restart_requested = False

            try:
                assert process.stdout is not None
                while not self._stop_event.is_set() and not self._restart_event.is_set():
                    chunk = process.stdout.read(64 * 1024)
                    if not chunk:
                        break
                    frame_buffer.extend(chunk)
                    for frame in self._extract_jpeg_frames(frame_buffer):
                        if self._stop_event.is_set() or self._restart_event.is_set():
                            break
                        self._publish_frame(frame)
                        frames_this_pass += 1
                        if first_process:
                            callbacks.first_frame(0)
                            first_process = False
                        elif loop_pending:
                            callbacks.loop_restart_completed()
                            callbacks.position_changed(0)
                            loop_pending = False
                        if self._restart_event.is_set():
                            break
            except (OSError, ValueError):
                if not self._stop_event.is_set() and not self._restart_event.is_set():
                    callbacks.failed()
                    self._finish_process(process, progress_thread)
                    return

            if self._restart_event.is_set():
                self._restart_event.clear()
                restart_requested = True
            self._finish_process(process, progress_thread)

            if self._stop_event.is_set():
                return
            if restart_requested:
                first_process = True
                loop_pending = False
                continue

            if process.returncode != 0 or frames_this_pass == 0:
                callbacks.failed()
                return

            callbacks.loop_restart_started()
            loop_pending = True
            first_process = False

    def _read_progress(
        self, process: subprocess.Popen, callbacks: PlaybackCallbacks
    ) -> None:
        if process.stderr is None:
            return
        while not self._stop_event.is_set():
            try:
                line = process.stderr.readline()
            except OSError:
                return
            if not line:
                return
            try:
                key, _, value = line.decode("ascii", errors="ignore").strip().partition("=")
                if key == "out_time_us":
                    callbacks.position_changed(max(int(value) // 1000, 0))
            except (ValueError, OSError):
                continue

    def _publish_frame(self, frame: bytes) -> None:
        with self._frame_condition:
            self._frame_sequence += 1
            self._latest_frame = frame
            self._frame_condition.notify_all()

    def _terminate_process(self) -> None:
        with self._lock:
            process = self._process
        if process is not None and process.poll() is None:
            try:
                process.terminate()
            except OSError:
                pass

    def _kill_process(self) -> None:
        with self._lock:
            process = self._process
        if process is not None and process.poll() is None:
            try:
                process.kill()
            except OSError:
                pass

    def _finish_process(
        self, process: subprocess.Popen, progress_thread: threading.Thread
    ) -> None:
        try:
            process.wait(timeout=self._join_timeout_seconds)
        except subprocess.TimeoutExpired:
            try:
                process.kill()
            except OSError:
                pass
            try:
                process.wait(timeout=self._join_timeout_seconds)
            except subprocess.TimeoutExpired:
                pass
        progress_thread.join(timeout=self._join_timeout_seconds)
        with self._lock:
            if self._process is process:
                self._process = None
