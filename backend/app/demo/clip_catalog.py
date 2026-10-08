"""Discover, validate, and prepare local virtual-CCTV video sources."""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from fractions import Fraction
import json
import os
from pathlib import Path
import queue
import subprocess
import threading
from typing import Any
from uuid import NAMESPACE_URL, uuid4, uuid5


DEMO_MEDIA_ROOT_ENV = "SENTINEL_DEMO_MEDIA_ROOT"
FFMPEG_BINARY_ENV = "SENTINEL_FFMPEG_BINARY"
FFPROBE_BINARY_ENV = "SENTINEL_FFPROBE_BINARY"
SUPPORTED_EXTENSIONS = {".mp4", ".mov", ".m4v", ".mkv", ".avi", ".webm"}
INTERNAL_DIRECTORY = ".sentinel"
CACHE_SCHEMA_VERSION = "1"


class DemoCatalogError(ValueError):
    """Safe configuration or lookup failure for the local demo catalog."""


class DemoClipNotFound(DemoCatalogError):
    """The requested opaque clip ID is not present in the ingest directory."""


class DemoClipNotReady(DemoCatalogError):
    """The source exists but is not yet a validated canonical video."""

    def __init__(self, state: str) -> None:
        super().__init__("The requested demo video is not ready.")
        self.state = state


@dataclass(frozen=True)
class MediaInfo:
    width: int
    height: int
    fps: float
    codec: str
    pixel_format: str
    container: str
    duration_seconds: float | None
    constant_frame_rate: bool = True

    def to_public_dict(self) -> dict[str, object]:
        return {
            "width": self.width,
            "height": self.height,
            "fps": round(self.fps, 3),
            "codec": self.codec,
            "pixel_format": self.pixel_format,
            "container": self.container,
            "duration_seconds": self.duration_seconds,
            "constant_frame_rate": self.constant_frame_rate,
        }


@dataclass(frozen=True)
class SourceFingerprint:
    relative_path: str
    size: int
    modified_ns: int


@dataclass(frozen=True)
class DemoClip:
    clip_id: str
    display_name: str
    relative_path: str
    resolved_path: Path | None
    state: str = "ready"
    normalization: str | None = None
    media: MediaInfo | None = None
    reason: str | None = None
    fingerprint: SourceFingerprint | None = None

    def to_public_dict(self) -> dict[str, object]:
        """Return safe ingest metadata without any local path."""
        return {
            "clip_id": self.clip_id,
            "display_name": self.display_name,
            "state": self.state,
            "normalization": self.normalization,
            "media": self.media.to_public_dict() if self.media else None,
            "reason": self.reason,
        }


class DemoClipCatalog:
    """Process-local folder catalog with one bounded normalization worker."""

    def __init__(
        self,
        media_root: Path | str,
        *,
        ffmpeg_binary: str | None = None,
        ffprobe_binary: str | None = None,
        stability_seconds: float = 0.75,
    ) -> None:
        self._media_root = Path(media_root).expanduser()
        self._ffmpeg_binary = ffmpeg_binary or os.environ.get(FFMPEG_BINARY_ENV, "ffmpeg")
        self._ffprobe_binary = ffprobe_binary or os.environ.get(
            FFPROBE_BINARY_ENV, self._derive_ffprobe(self._ffmpeg_binary)
        )
        self._stability_seconds = max(0.0, stability_seconds)
        self._lock = threading.RLock()
        self._records: dict[str, DemoClip] = {}
        self._pending: set[str] = set()
        self._jobs: queue.Queue[tuple[str, SourceFingerprint] | None] = queue.Queue()
        self._worker: threading.Thread | None = None
        self._stop_event = threading.Event()
        self._process: subprocess.Popen[str] | None = None
        self._startup_temp_reconciled = False

    @classmethod
    def from_environment(cls) -> "DemoClipCatalog":
        configured_root = os.environ.get(DEMO_MEDIA_ROOT_ENV, "").strip()
        if not configured_root:
            raise DemoCatalogError(f"Demo media is not configured; set {DEMO_MEDIA_ROOT_ENV}.")
        return cls(configured_root)

    def list_clips(self) -> list[DemoClip]:
        """Reconcile top-level source files and return current ingest records."""
        root = self._resolve_root()
        self._ensure_internal_directories(root)
        self._reconcile_startup_temp(root)
        discovered: set[str] = set()
        try:
            entries = sorted(root.iterdir(), key=lambda item: item.name.casefold())
        except OSError as exc:
            raise DemoCatalogError("Configured demo media root is unavailable.") from exc

        for source_path in entries:
            if source_path.name == INTERNAL_DIRECTORY or source_path.is_dir():
                continue
            if source_path.suffix.casefold() not in SUPPORTED_EXTENSIONS:
                continue
            relative_path = source_path.name
            clip_id = self._clip_id(relative_path)
            discovered.add(clip_id)
            try:
                resolved_source = source_path.resolve(strict=True)
                resolved_source.relative_to(root)
                stat = resolved_source.stat()
                fingerprint = SourceFingerprint(relative_path, stat.st_size, stat.st_mtime_ns)
            except (OSError, RuntimeError, ValueError):
                self._set_record(DemoClip(
                    clip_id, relative_path, relative_path, None,
                    state="rejected",
                    reason="Source is unavailable or outside the media directory.",
                ))
                continue

            with self._lock:
                existing = self._records.get(clip_id)
            if existing is not None and existing.fingerprint == fingerprint:
                if existing.state == "waiting_for_file":
                    self._queue_prepare(clip_id, fingerprint)
                continue

            if existing is not None:
                self._remove_cached_derivative(root, clip_id)
            cached = self._load_cached_record(root, clip_id, fingerprint)
            if cached is not None:
                self._set_record(cached)
                continue
            if existing is None:
                self._remove_cached_derivative(root, clip_id)
            self._set_record(DemoClip(
                clip_id, relative_path, relative_path, None,
                state="waiting_for_file",
                reason="Waiting for the file copy to finish.",
                fingerprint=fingerprint,
            ))
            self._queue_prepare(clip_id, fingerprint)

        with self._lock:
            removed = set(self._records) - discovered
            for clip_id in removed:
                self._records.pop(clip_id, None)
                self._pending.discard(clip_id)
                self._remove_cached_derivative(root, clip_id)
            return sorted(self._records.values(), key=lambda clip: clip.display_name.casefold())

    def get_clip(self, clip_id: str) -> DemoClip:
        if not isinstance(clip_id, str) or not clip_id.strip():
            raise DemoClipNotFound("Unknown demo clip ID.")
        for clip in self.list_clips():
            if clip.clip_id != clip_id:
                continue
            if clip.state != "ready" or clip.resolved_path is None:
                raise DemoClipNotReady(clip.state)
            self._validate_ready_clip(clip)
            return clip
        raise DemoClipNotFound("Unknown demo clip ID.")

    def counts(self) -> dict[str, int]:
        clips = self.list_clips()
        return {
            "input_videos": len(clips),
            "ready": sum(clip.state == "ready" for clip in clips),
            "preparing": sum(clip.state in {"waiting_for_file", "validating", "transcoding"} for clip in clips),
            "rejected": sum(clip.state in {"rejected", "failed"} for clip in clips),
        }

    def shutdown(self) -> None:
        """Stop only this catalog's worker and active normalization process."""
        self._stop_event.set()
        self._jobs.put(None)
        with self._lock:
            process, worker = self._process, self._worker
        if process is not None and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=3)
        if worker is not None and worker is not threading.current_thread():
            worker.join(timeout=5)
        with self._lock:
            self._process = None
            self._worker = None
        try:
            self._clear_partial_outputs(self._resolve_root())
        except DemoCatalogError:
            pass

    @staticmethod
    def _derive_ffprobe(ffmpeg_binary: str) -> str:
        path = Path(ffmpeg_binary)
        if path.name.casefold() in {"ffmpeg", "ffmpeg.exe"} and path.parent != Path("."):
            candidate = path.with_name("ffprobe" + path.suffix)
            if candidate.is_file():
                return str(candidate)
        return "ffprobe"

    @staticmethod
    def _clip_id(relative_path: str) -> str:
        normalized = relative_path.replace("\\", "/").casefold()
        return f"demo-{uuid5(NAMESPACE_URL, 'sentinel-demo-media/' + normalized).hex}"

    def _resolve_root(self) -> Path:
        if not self._media_root.is_absolute():
            raise DemoCatalogError("Configured demo media root must be absolute.")
        try:
            root = self._media_root.resolve(strict=True)
        except (OSError, RuntimeError) as exc:
            raise DemoCatalogError("Configured demo media root is unavailable.") from exc
        if not root.is_dir():
            raise DemoCatalogError("Configured demo media root is not a directory.")
        return root

    @staticmethod
    def _ensure_internal_directories(root: Path) -> None:
        try:
            for relative in ("processed", "metadata", "temp"):
                (root / INTERNAL_DIRECTORY / relative).mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise DemoCatalogError("Sentinel media cache could not be initialized.") from exc

    def _reconcile_startup_temp(self, root: Path) -> None:
        with self._lock:
            if self._startup_temp_reconciled:
                return
            self._startup_temp_reconciled = True
        self._clear_partial_outputs(root)

    @staticmethod
    def _clear_partial_outputs(root: Path) -> None:
        temp_root = root / INTERNAL_DIRECTORY / "temp"
        try:
            for partial in temp_root.glob("*.partial.mp4"):
                partial.unlink(missing_ok=True)
        except OSError:
            pass

    def _queue_prepare(self, clip_id: str, fingerprint: SourceFingerprint) -> None:
        with self._lock:
            if clip_id in self._pending or self._stop_event.is_set():
                return
            self._pending.add(clip_id)
            if self._worker is None or not self._worker.is_alive():
                self._worker = threading.Thread(target=self._worker_loop, name="sentinel-media-ingest", daemon=True)
                self._worker.start()
        self._jobs.put((clip_id, fingerprint))

    def _worker_loop(self) -> None:
        while not self._stop_event.is_set():
            job = self._jobs.get()
            if job is None:
                return
            clip_id, fingerprint = job
            try:
                self._prepare(clip_id, fingerprint)
            finally:
                with self._lock:
                    self._pending.discard(clip_id)

    def _prepare(self, clip_id: str, fingerprint: SourceFingerprint) -> None:
        root = self._resolve_root()
        source = root / fingerprint.relative_path
        if self._stop_event.wait(self._stability_seconds):
            return
        try:
            current = source.resolve(strict=True)
            current.relative_to(root)
            stat = current.stat()
        except (OSError, RuntimeError, ValueError):
            self._update_state(clip_id, "rejected", "Source became unavailable.")
            return
        if stat.st_size != fingerprint.size or stat.st_mtime_ns != fingerprint.modified_ns:
            self._update_state(clip_id, "waiting_for_file", "Waiting for the file copy to finish.")
            return
        if stat.st_size == 0:
            self._update_state(clip_id, "rejected", "Media file is empty.")
            return

        self._update_state(clip_id, "validating", None)
        try:
            source_media = self._probe(current)
        except DemoCatalogError as exc:
            self._update_state(clip_id, "rejected", str(exc))
            return
        if self._is_canonical(source_media):
            ready = DemoClip(
                clip_id, fingerprint.relative_path, fingerprint.relative_path, current,
                state="ready", normalization="direct_validated", media=source_media,
                fingerprint=fingerprint,
            )
            self._set_record(ready)
            self._write_metadata(root, ready)
            return

        self._update_state(clip_id, "transcoding", None)
        processed = root / INTERNAL_DIRECTORY / "processed" / f"{clip_id}.mp4"
        partial = root / INTERNAL_DIRECTORY / "temp" / f"{clip_id}-{uuid4().hex}.partial.mp4"
        command = [
            self._ffmpeg_binary, "-hide_banner", "-loglevel", "error", "-y", "-i", str(current),
            "-map", "0:v:0", "-an", "-vf",
            "scale=1280:720:force_original_aspect_ratio=decrease:out_range=tv,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30,format=yuv420p",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p", "-color_range", "tv",
            "-movflags", "+faststart", str(partial),
        ]
        try:
            process = subprocess.Popen(
                command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE, text=True, encoding="utf-8",
            )
            with self._lock:
                self._process = process
            process.communicate()
            with self._lock:
                if self._process is process:
                    self._process = None
            if self._stop_event.is_set():
                partial.unlink(missing_ok=True)
                return
            if process.returncode != 0:
                raise DemoCatalogError("Video normalization failed.")
            normalized_media = self._probe(partial)
            if not self._is_canonical(normalized_media):
                raise DemoCatalogError("Normalized video failed canonical validation.")
            os.replace(partial, processed)
            ready = DemoClip(
                clip_id, fingerprint.relative_path, fingerprint.relative_path, processed,
                state="ready", normalization="transcoded", media=normalized_media,
                fingerprint=fingerprint,
            )
            self._set_record(ready)
            self._write_metadata(root, ready)
        except (OSError, subprocess.SubprocessError, DemoCatalogError):
            partial.unlink(missing_ok=True)
            self._update_state(clip_id, "failed", "Video normalization failed.")

    def _probe(self, path: Path) -> MediaInfo:
        command = [
            self._ffprobe_binary, "-v", "error", "-select_streams", "v:0",
            "-show_entries",
            "stream=codec_name,width,height,pix_fmt,avg_frame_rate,r_frame_rate,duration:format=format_name,duration",
            "-of", "json", str(path),
        ]
        try:
            completed = subprocess.run(
                command, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                encoding="utf-8", timeout=30, check=False,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            raise DemoCatalogError("Media inspection is unavailable.") from exc
        if completed.returncode != 0:
            raise DemoCatalogError("Media could not be decoded.")
        try:
            payload = json.loads(completed.stdout)
            streams = payload.get("streams", [])
            if not streams:
                raise ValueError("missing video stream")
            stream = streams[0]
            width, height = int(stream["width"]), int(stream["height"])
            codec = str(stream["codec_name"]).casefold()
            pixel_format = str(stream.get("pix_fmt") or "").casefold()
            avg_fps = self._parse_rate(stream.get("avg_frame_rate"))
            real_fps = self._parse_rate(stream.get("r_frame_rate"))
            fps = avg_fps or real_fps
            constant_frame_rate = bool(avg_fps and real_fps and abs(avg_fps - real_fps) < 0.01)
            formats = payload.get("format", {})
            container = str(formats.get("format_name") or "").casefold()
            raw_duration = stream.get("duration") or formats.get("duration")
            duration = float(raw_duration) if raw_duration not in {None, "N/A"} else None
        except (KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
            raise DemoCatalogError("Media video metadata is invalid.") from exc
        if width <= 0 or height <= 0 or fps <= 0:
            raise DemoCatalogError("Media video metadata is invalid.")
        return MediaInfo(width, height, fps, codec, pixel_format, container, duration, constant_frame_rate)

    @staticmethod
    def _parse_rate(value: Any) -> float:
        if not value or value == "0/0":
            return 0.0
        return float(Fraction(str(value)))

    @staticmethod
    def _is_canonical(media: MediaInfo) -> bool:
        return (
            "mp4" in set(media.container.split(",")) and media.codec == "h264"
            and media.pixel_format == "yuv420p" and media.width == 1280
            and media.height == 720 and abs(media.fps - 30.0) < 0.01
            and media.constant_frame_rate
        )

    def _validate_ready_clip(self, clip: DemoClip) -> None:
        root = self._resolve_root()
        assert clip.resolved_path is not None
        try:
            resolved = clip.resolved_path.resolve(strict=True)
            resolved.relative_to(root)
            source = (root / clip.relative_path).resolve(strict=True)
            source.relative_to(root)
            stat = source.stat()
        except (OSError, RuntimeError, ValueError) as exc:
            raise DemoClipNotReady("unavailable") from exc
        fingerprint = clip.fingerprint
        if fingerprint is None or stat.st_size != fingerprint.size or stat.st_mtime_ns != fingerprint.modified_ns:
            raise DemoClipNotReady("changed")

    def _set_record(self, clip: DemoClip) -> None:
        with self._lock:
            self._records[clip.clip_id] = clip

    def _update_state(self, clip_id: str, state: str, reason: str | None) -> None:
        with self._lock:
            current = self._records.get(clip_id)
            if current is not None:
                self._records[clip_id] = replace(current, state=state, resolved_path=None, reason=reason)

    def _write_metadata(self, root: Path, clip: DemoClip) -> None:
        assert clip.fingerprint is not None and clip.media is not None
        path = root / INTERNAL_DIRECTORY / "metadata" / f"{clip.clip_id}.json"
        temporary = path.with_suffix(".json.tmp")
        payload = {
            "schema_version": CACHE_SCHEMA_VERSION,
            "clip_id": clip.clip_id,
            "fingerprint": asdict(clip.fingerprint),
            "normalization": clip.normalization,
            "media": asdict(clip.media),
        }
        temporary.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
        os.replace(temporary, path)

    def _load_cached_record(self, root: Path, clip_id: str, fingerprint: SourceFingerprint) -> DemoClip | None:
        path = root / INTERNAL_DIRECTORY / "metadata" / f"{clip_id}.json"
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            if payload.get("schema_version") != CACHE_SCHEMA_VERSION:
                return None
            if SourceFingerprint(**payload["fingerprint"]) != fingerprint:
                return None
            normalization = payload["normalization"]
            media = MediaInfo(**payload["media"])
            resolved = (
                root / fingerprint.relative_path
                if normalization == "direct_validated"
                else root / INTERNAL_DIRECTORY / "processed" / f"{clip_id}.mp4"
            ).resolve(strict=True)
            resolved.relative_to(root)
            if not resolved.is_file():
                return None
            return DemoClip(
                clip_id, fingerprint.relative_path, fingerprint.relative_path, resolved,
                state="ready", normalization=normalization, media=media, fingerprint=fingerprint,
            )
        except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError):
            return None

    @staticmethod
    def _remove_cached_derivative(root: Path, clip_id: str) -> None:
        for path in (
            root / INTERNAL_DIRECTORY / "processed" / f"{clip_id}.mp4",
            root / INTERNAL_DIRECTORY / "metadata" / f"{clip_id}.json",
        ):
            try:
                path.unlink(missing_ok=True)
            except OSError:
                pass
