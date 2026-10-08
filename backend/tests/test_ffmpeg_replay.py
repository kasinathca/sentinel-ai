from __future__ import annotations

from collections import deque
from io import BytesIO
from pathlib import Path
import subprocess
import threading
import unittest

from app.demo.clip_catalog import DemoClip
from app.demo.controller import PlaybackCallbacks
from app.demo.ffmpeg_replay import FFmpegReplayAdapter, MAX_JPEG_FRAME_BYTES


JPEG_ONE = b"\xff\xd8frame-one\xff\xd9"
JPEG_TWO = b"\xff\xd8frame-two\xff\xd9"


class FakeStdout:
    def __init__(self, process: "FakeProcess") -> None:
        self.process = process
        self.chunks = deque(process.chunks)

    def read(self, _size: int) -> bytes:
        if self.chunks:
            return self.chunks.popleft()
        if self.process.block_after_output:
            self.process.exited.wait()
        else:
            self.process.finish(self.process.natural_returncode)
        return b""


class FakeProcess:
    def __init__(
        self,
        chunks: list[bytes] | None = None,
        *,
        natural_returncode: int = 0,
        block_after_output: bool = False,
        ignore_terminate: bool = False,
    ) -> None:
        self.chunks = chunks or []
        self.natural_returncode = natural_returncode
        self.block_after_output = block_after_output
        self.ignore_terminate = ignore_terminate
        self.exited = threading.Event()
        self.returncode: int | None = None
        self.terminate_count = 0
        self.kill_count = 0
        self.stdout = FakeStdout(self)
        self.stderr = BytesIO(b"out_time_us=1000000\n")

    def poll(self) -> int | None:
        return self.returncode

    def wait(self, timeout: float | None = None) -> int:
        if self.returncode is not None:
            return self.returncode
        if not self.exited.wait(timeout):
            raise subprocess.TimeoutExpired("fake-ffmpeg", timeout)
        assert self.returncode is not None
        return self.returncode

    def terminate(self) -> None:
        self.terminate_count += 1
        if not self.ignore_terminate:
            self.finish(-15)

    def kill(self) -> None:
        self.kill_count += 1
        self.finish(-9)

    def finish(self, code: int) -> None:
        if self.returncode is None:
            self.returncode = code
        self.exited.set()


class QueueProcessFactory:
    def __init__(self, processes: list[FakeProcess | BaseException]) -> None:
        self.pending = deque(processes)
        self.created: list[FakeProcess] = []
        self.commands: list[list[str]] = []

    def __call__(self, command, **_kwargs):
        self.commands.append(command)
        result = self.pending.popleft()
        if isinstance(result, BaseException):
            raise result
        self.created.append(result)
        return result


class RecordingCallbacks(PlaybackCallbacks):
    def __init__(self) -> None:
        self.first_frame_event = threading.Event()
        self.loop_started_event = threading.Event()
        self.loop_completed_event = threading.Event()
        self.failed_event = threading.Event()
        self.first_frame_count = 0
        self.loop_started_count = 0
        self.loop_completed_count = 0
        self.positions: list[int] = []
        self._lock = threading.Lock()

    def first_frame(self, position_ms: int = 0) -> None:
        with self._lock:
            self.first_frame_count += 1
            self.positions.append(position_ms)
        self.first_frame_event.set()

    def position_changed(self, position_ms: int) -> None:
        with self._lock:
            self.positions.append(position_ms)

    def loop_restart_started(self) -> None:
        self.loop_started_count += 1
        self.loop_started_event.set()

    def loop_restart_completed(self) -> None:
        self.loop_completed_count += 1
        self.loop_completed_event.set()

    def failed(self) -> None:
        self.failed_event.set()


class FFmpegReplayTests(unittest.TestCase):
    def setUp(self) -> None:
        self.clip = DemoClip(
            clip_id="approved-demo",
            display_name="Approved demo",
            relative_path="clips/demo.mp4",
            resolved_path=Path("C:/approved-media/clips/demo.mp4"),
        )

    def _adapter(self, factory: QueueProcessFactory) -> FFmpegReplayAdapter:
        return FFmpegReplayAdapter(
            "ffmpeg", process_factory=factory, join_timeout_seconds=0.02
        )

    def test_command_uses_natural_rate_and_jpeg_pipe(self) -> None:
        adapter = self._adapter(QueueProcessFactory([]))
        command = adapter._build_command(self.clip)
        self.assertIn("-re", command)
        self.assertIn("image2pipe", command)
        self.assertIn("mjpeg", command)
        self.assertEqual(command[-1], "pipe:1")
        self.assertIn(str(self.clip.resolved_path), command)

    def test_jpeg_extractor_handles_partial_and_concatenated_frames(self) -> None:
        buffer = bytearray(b"noise\xff\xd8first")
        self.assertEqual(FFmpegReplayAdapter._extract_jpeg_frames(buffer), [])
        buffer.extend(b"\xff\xd9\xff\xd8second\xff\xd9tail")
        frames = FFmpegReplayAdapter._extract_jpeg_frames(buffer)
        self.assertEqual(
            frames,
            [b"\xff\xd8first\xff\xd9", b"\xff\xd8second\xff\xd9"],
        )
        self.assertEqual(buffer, bytearray(b"l"))

    def test_oversized_unterminated_frame_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            FFmpegReplayAdapter._extract_jpeg_frames(
                bytearray(b"\xff\xd8" + b"x" * (MAX_JPEG_FRAME_BYTES + 1))
            )

    def test_first_valid_frame_is_published_and_reported_once(self) -> None:
        process = FakeProcess([JPEG_ONE], block_after_output=True)
        factory = QueueProcessFactory([process])
        adapter = self._adapter(factory)
        callbacks = RecordingCallbacks()
        adapter.start(self.clip, callbacks)
        try:
            self.assertTrue(callbacks.first_frame_event.wait(1.0))
            self.assertEqual(adapter.wait_for_frame(0, 0.1), (1, JPEG_ONE))
            self.assertEqual(callbacks.first_frame_count, 1)
            self.assertFalse(callbacks.failed_event.is_set())
        finally:
            adapter.stop()

    def test_natural_eof_restarts_and_second_pass_completes_loop(self) -> None:
        first = FakeProcess([JPEG_ONE])
        second = FakeProcess([JPEG_TWO], block_after_output=True)
        factory = QueueProcessFactory([first, second])
        adapter = self._adapter(factory)
        callbacks = RecordingCallbacks()
        adapter.start(self.clip, callbacks)
        try:
            self.assertTrue(callbacks.loop_started_event.wait(1.0))
            self.assertTrue(callbacks.loop_completed_event.wait(1.0))
            frame = adapter.wait_for_frame(1, 0.1)
            self.assertIsNotNone(frame)
            self.assertEqual(frame, (2, JPEG_TWO))
            self.assertEqual(len(factory.created), 2)
            self.assertFalse(callbacks.failed_event.is_set())
        finally:
            adapter.stop()

    def test_explicit_restart_terminates_old_process_without_eof_loop(self) -> None:
        first = FakeProcess([JPEG_ONE], block_after_output=True)
        second = FakeProcess([JPEG_TWO], block_after_output=True)
        factory = QueueProcessFactory([first, second])
        adapter = self._adapter(factory)
        old_callbacks = RecordingCallbacks()
        new_callbacks = RecordingCallbacks()
        adapter.start(self.clip, old_callbacks)
        try:
            self.assertTrue(old_callbacks.first_frame_event.wait(1.0))
            adapter.restart(new_callbacks)
            self.assertTrue(new_callbacks.first_frame_event.wait(1.0))
            self.assertEqual(len(factory.created), 2)
            self.assertEqual(first.terminate_count, 1)
            self.assertEqual(old_callbacks.loop_started_count, 0)
            self.assertEqual(new_callbacks.loop_started_count, 0)
            self.assertFalse(new_callbacks.failed_event.is_set())
        finally:
            adapter.stop()

    def test_stop_clears_frame_notifies_waiters_and_prevents_next_loop(self) -> None:
        process = FakeProcess([JPEG_ONE], block_after_output=True)
        factory = QueueProcessFactory([process])
        adapter = self._adapter(factory)
        callbacks = RecordingCallbacks()
        adapter.start(self.clip, callbacks)
        self.assertTrue(callbacks.first_frame_event.wait(1.0))
        adapter.stop()
        self.assertEqual(process.terminate_count, 1)
        self.assertIsNone(adapter._latest_frame)
        self.assertIsNone(adapter.wait_for_frame(1, 0.1))
        self.assertEqual(len(factory.created), 1)
        self.assertFalse(adapter._worker.is_alive())

    def test_spawn_failure_calls_failed_and_exits_worker(self) -> None:
        factory = QueueProcessFactory([OSError("ffmpeg missing")])
        adapter = self._adapter(factory)
        callbacks = RecordingCallbacks()
        adapter.start(self.clip, callbacks)
        self.assertTrue(callbacks.failed_event.wait(1.0))
        adapter._worker.join(1.0)
        self.assertFalse(adapter._worker.is_alive())
        self.assertFalse(callbacks.first_frame_event.is_set())

    def test_nonzero_exit_calls_failed_without_automatic_loop(self) -> None:
        process = FakeProcess([], natural_returncode=2)
        factory = QueueProcessFactory([process])
        adapter = self._adapter(factory)
        callbacks = RecordingCallbacks()
        adapter.start(self.clip, callbacks)
        self.assertTrue(callbacks.failed_event.wait(1.0))
        self.assertEqual(len(factory.created), 1)
        self.assertEqual(callbacks.loop_started_count, 0)
        self.assertFalse(callbacks.first_frame_event.is_set())

    def test_zero_frame_successful_exit_is_failure(self) -> None:
        process = FakeProcess([], natural_returncode=0)
        factory = QueueProcessFactory([process])
        adapter = self._adapter(factory)
        callbacks = RecordingCallbacks()
        adapter.start(self.clip, callbacks)
        self.assertTrue(callbacks.failed_event.wait(1.0))
        self.assertEqual(len(factory.created), 1)
        self.assertEqual(callbacks.loop_started_count, 0)

    def test_parser_failure_terminates_process_and_reports_failure(self) -> None:
        oversized = b"\xff\xd8" + b"x" * (MAX_JPEG_FRAME_BYTES + 1)
        process = FakeProcess([oversized], block_after_output=True)
        factory = QueueProcessFactory([process])
        adapter = self._adapter(factory)
        callbacks = RecordingCallbacks()
        adapter.start(self.clip, callbacks)
        self.assertTrue(callbacks.failed_event.wait(1.0))
        self.assertEqual(process.terminate_count, 1)
        adapter._worker.join(1.0)
        self.assertFalse(adapter._worker.is_alive())

    def test_stop_uses_kill_fallback_when_terminate_is_ignored(self) -> None:
        process = FakeProcess(
            [JPEG_ONE], block_after_output=True, ignore_terminate=True
        )
        factory = QueueProcessFactory([process])
        adapter = self._adapter(factory)
        callbacks = RecordingCallbacks()
        adapter.start(self.clip, callbacks)
        self.assertTrue(callbacks.first_frame_event.wait(1.0))
        adapter.stop()
        self.assertEqual(process.terminate_count, 1)
        self.assertEqual(process.kill_count, 1)
        self.assertFalse(adapter._worker.is_alive())


if __name__ == "__main__":
    unittest.main()
