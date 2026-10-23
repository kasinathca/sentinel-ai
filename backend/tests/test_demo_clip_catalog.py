from __future__ import annotations

from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

from app.demo.clip_catalog import (
    DemoCatalogError,
    DemoClipCatalog,
    DemoClipNotFound,
    DemoClipNotReady,
    MediaInfo,
)


CANONICAL = MediaInfo(1280, 720, 30.0, "h264", "yuv420p", "mov,mp4", 2.0)
WIDE = MediaInfo(1920, 1080, 29.97, "h264", "yuv420p", "mov,mp4", 2.0)
PORTRAIT = MediaInfo(720, 1280, 25.0, "hevc", "yuv420p", "mov", 2.0)


class ControlledCatalog(DemoClipCatalog):
    def __init__(self, root: Path, media_by_name: dict[str, MediaInfo | Exception], **kwargs) -> None:
        super().__init__(root, stability_seconds=kwargs.pop("stability_seconds", 0.01), **kwargs)
        self.media_by_name = media_by_name
        self.probe_calls: list[str] = []

    def _probe(self, path: Path) -> MediaInfo:
        self.probe_calls.append(path.name)
        if ".partial.mp4" in path.name:
            return CANONICAL
        value = self.media_by_name.get(path.name, CANONICAL)
        if isinstance(value, Exception):
            raise value
        return value


class BadOutputCatalog(ControlledCatalog):
    def _probe(self, path: Path) -> MediaInfo:
        if ".partial.mp4" in path.name:
            return WIDE
        return super()._probe(path)


class FakeFFmpegProcess:
    returncode = 0

    def __init__(self, command, **kwargs) -> None:
        del kwargs
        Path(command[-1]).write_bytes(b"canonical derivative")
        self._finished = False

    def communicate(self):
        self._finished = True
        return "", ""

    def poll(self):
        return self.returncode if self._finished else None

    def terminate(self) -> None:
        self.returncode = 1
        self._finished = True

    def kill(self) -> None:
        self.terminate()

    def wait(self, timeout=None):
        del timeout
        return self.returncode


class FailingFFmpegProcess(FakeFFmpegProcess):
    returncode = 1


class DemoClipCatalogTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.catalogs: list[DemoClipCatalog] = []

    def tearDown(self) -> None:
        for catalog in self.catalogs:
            catalog.shutdown()
        self.temp_dir.cleanup()

    def catalog(self, media: dict[str, MediaInfo | Exception], **kwargs) -> ControlledCatalog:
        catalog = ControlledCatalog(self.root, media, **kwargs)
        self.catalogs.append(catalog)
        return catalog

    def wait_for(self, catalog: DemoClipCatalog, name: str, states=("ready",), timeout=2.0):
        deadline = time.monotonic() + timeout
        latest = None
        while time.monotonic() < deadline:
            latest = next((clip for clip in catalog.list_clips() if clip.display_name == name), None)
            if latest is not None and latest.state in states:
                return latest
            time.sleep(0.01)
        self.fail(f"{name} did not reach {states}; latest={latest}")

    def test_canonical_top_level_video_is_discovered_without_manifest(self) -> None:
        (self.root / "ordinary video.mp4").write_bytes(b"source")
        catalog = self.catalog({"ordinary video.mp4": CANONICAL})

        clip = self.wait_for(catalog, "ordinary video.mp4")

        self.assertEqual(clip.normalization, "direct_validated")
        self.assertEqual(clip.resolved_path, self.root / "ordinary video.mp4")
        self.assertEqual(clip.media, CANONICAL)
        self.assertNotIn(str(self.root), str(clip.to_public_dict()))
        self.assertTrue(clip.clip_id.startswith("demo-"))
        self.assertEqual(catalog.get_clip(clip.clip_id), clip)

    @patch("app.demo.clip_catalog.subprocess.Popen", FakeFFmpegProcess)
    def test_noncanonical_video_is_normalized_atomically_and_original_preserved(self) -> None:
        original = self.root / "phone (portrait) Ω.mov"
        original.write_bytes(b"original bytes")
        catalog = self.catalog({original.name: PORTRAIT})

        clip = self.wait_for(catalog, original.name)

        self.assertEqual(original.read_bytes(), b"original bytes")
        self.assertEqual(clip.normalization, "transcoded")
        self.assertEqual(clip.media, CANONICAL)
        self.assertIn(".sentinel", clip.resolved_path.parts)
        self.assertEqual(clip.resolved_path.read_bytes(), b"canonical derivative")
        self.assertFalse(list((self.root / ".sentinel" / "temp").glob("*.partial.mp4")))

    def test_invalid_zero_byte_audio_or_corrupt_inputs_do_not_break_good_video(self) -> None:
        names = ["empty.mp4", "text.mp4", "audio.mp4", "good.mp4"]
        for name in names:
            (self.root / name).write_bytes(b"" if name == "empty.mp4" else b"bytes")
        invalid = DemoCatalogError("Media could not be decoded.")
        catalog = self.catalog({"text.mp4": invalid, "audio.mp4": invalid, "good.mp4": CANONICAL})

        good = self.wait_for(catalog, "good.mp4")
        empty = self.wait_for(catalog, "empty.mp4", ("rejected",))
        text = self.wait_for(catalog, "text.mp4", ("rejected",))
        audio = self.wait_for(catalog, "audio.mp4", ("rejected",))

        self.assertEqual(good.state, "ready")
        self.assertEqual(empty.reason, "Media file is empty.")
        self.assertEqual(text.reason, "Media could not be decoded.")
        self.assertEqual(audio.reason, "Media could not be decoded.")

    def test_unsupported_nested_and_internal_files_are_not_discovered(self) -> None:
        (self.root / "notes.txt").write_text("not video", encoding="utf-8")
        (self.root / "nested").mkdir()
        (self.root / "nested" / "hidden.mp4").write_bytes(b"video")
        (self.root / ".sentinel").mkdir()
        (self.root / ".sentinel" / "internal.mp4").write_bytes(b"video")
        catalog = self.catalog({})

        self.assertEqual(catalog.list_clips(), [])

    def test_startup_removes_only_stale_partial_normalization_outputs(self) -> None:
        temp_root = self.root / ".sentinel" / "temp"
        temp_root.mkdir(parents=True)
        stale = temp_root / "interrupted.partial.mp4"
        unrelated = temp_root / "operator-note.txt"
        stale.write_bytes(b"incomplete")
        unrelated.write_text("preserve", encoding="utf-8")
        catalog = self.catalog({})

        self.assertEqual(catalog.list_clips(), [])

        self.assertFalse(stale.exists())
        self.assertEqual(unrelated.read_text(encoding="utf-8"), "preserve")

    def test_stable_id_cache_reuse_modified_source_and_deletion_cleanup(self) -> None:
        source = self.root / "banana_123.mp4"
        source.write_bytes(b"version one")
        first = self.catalog({source.name: CANONICAL})
        original = self.wait_for(first, source.name)
        original_id = original.clip_id
        first.shutdown()

        cached = self.catalog({source.name: DemoCatalogError("probe must not run")})
        reused = cached.list_clips()[0]
        self.assertEqual(reused.state, "ready")
        self.assertEqual(reused.clip_id, original_id)
        self.assertEqual(cached.probe_calls, [])

        source.write_bytes(b"version two is different")
        cached.media_by_name[source.name] = CANONICAL
        changed = self.wait_for(cached, source.name)
        self.assertEqual(changed.clip_id, original_id)
        self.assertIn(source.name, cached.probe_calls)

        source.unlink()
        self.assertEqual(cached.list_clips(), [])
        metadata = self.root / ".sentinel" / "metadata" / f"{original_id}.json"
        self.assertFalse(metadata.exists())

    def test_changing_file_waits_and_retries_after_stabilizing(self) -> None:
        source = self.root / "copying.webm"
        source.write_bytes(b"first")
        catalog = ControlledCatalog(self.root, {source.name: CANONICAL}, stability_seconds=0.08)
        self.catalogs.append(catalog)
        catalog.list_clips()
        time.sleep(0.02)
        source.write_bytes(b"still copying")

        waiting = self.wait_for(catalog, source.name, ("waiting_for_file",))
        self.assertEqual(waiting.state, "waiting_for_file")
        ready = self.wait_for(catalog, source.name, timeout=2.0)
        self.assertEqual(ready.state, "ready")

    @patch("app.demo.clip_catalog.subprocess.Popen", FailingFFmpegProcess)
    def test_ffmpeg_failure_preserves_original_and_never_marks_ready(self) -> None:
        source = self.root / "wide.mkv"
        source.write_bytes(b"original")
        catalog = self.catalog({source.name: WIDE})

        failed = self.wait_for(catalog, source.name, ("failed",))

        self.assertEqual(source.read_bytes(), b"original")
        self.assertEqual(failed.reason, "Video normalization failed.")
        self.assertFalse(list((self.root / ".sentinel" / "temp").glob("*")))

    def test_unknown_and_not_ready_ids_are_rejected(self) -> None:
        source = self.root / "new.mov"
        source.write_bytes(b"source")
        catalog = ControlledCatalog(self.root, {source.name: PORTRAIT}, stability_seconds=1)
        self.catalogs.append(catalog)
        clip = catalog.list_clips()[0]

        with self.assertRaises(DemoClipNotReady):
            catalog.get_clip(clip.clip_id)
        with self.assertRaises(DemoClipNotFound):
            catalog.get_clip("C:\\outside.mp4")

    def test_ffprobe_unavailable_is_an_explicit_rejected_state(self) -> None:
        source = self.root / "probe.mp4"
        source.write_bytes(b"source")
        catalog = DemoClipCatalog(
            self.root,
            ffprobe_binary="definitely-missing-sentinel-ffprobe",
            stability_seconds=0.01,
        )
        self.catalogs.append(catalog)

        rejected = self.wait_for(catalog, source.name, ("rejected",))

        self.assertEqual(rejected.reason, "Media inspection is unavailable.")

    def test_ffmpeg_unavailable_and_invalid_normalized_output_never_become_ready(self) -> None:
        source = self.root / "needs conversion.avi"
        source.write_bytes(b"source")
        missing = self.catalog(
            {source.name: WIDE}, ffmpeg_binary="definitely-missing-sentinel-ffmpeg"
        )
        self.assertEqual(
            self.wait_for(missing, source.name, ("failed",)).state, "failed"
        )

        source.write_bytes(b"changed source")
        invalid_output = BadOutputCatalog(self.root, {source.name: WIDE})
        self.catalogs.append(invalid_output)
        with patch("app.demo.clip_catalog.subprocess.Popen", FakeFFmpegProcess):
            failed = self.wait_for(invalid_output, source.name, ("failed",))
        self.assertEqual(failed.state, "failed")

    def test_relative_media_root_is_rejected(self) -> None:
        with self.assertRaisesRegex(DemoCatalogError, "must be absolute"):
            DemoClipCatalog(Path("relative-media-root")).list_clips()


if __name__ == "__main__":
    unittest.main()
