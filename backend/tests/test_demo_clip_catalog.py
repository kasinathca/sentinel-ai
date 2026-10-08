from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from app.demo.clip_catalog import (
    DemoCatalogError,
    DemoClipCatalog,
    DemoClipNotFound,
)


class DemoClipCatalogTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "fight").mkdir()
        (self.root / "fight" / "fight_01.mp4").write_bytes(b"test media")
        self.manifest = {
            "schema_version": "1",
            "clips": [
                {
                    "clip_id": "fight-01",
                    "relative_path": "fight/fight_01.mp4",
                    "display_name": "Scenario 01",
                    "expected_class": "fighting",
                    "sha256": "TBD_FROM_ACTUAL_FILE",
                    "duration_ms": None,
                    "provenance": "TBD",
                    "permission_status": "TBD",
                }
            ],
        }
        self._write_manifest()
        self.catalog = DemoClipCatalog(self.root)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _write_manifest(self) -> None:
        (self.root / "manifest.json").write_text(
            json.dumps(self.manifest), encoding="utf-8"
        )

    def test_list_returns_clip_without_exposing_filesystem_path(self) -> None:
        clips = self.catalog.list_clips()

        self.assertEqual(len(clips), 1)
        self.assertEqual(clips[0].resolved_path, self.root / "fight" / "fight_01.mp4")
        self.assertEqual(
            clips[0].to_public_dict(),
            {"clip_id": "fight-01", "display_name": "Scenario 01"},
        )
        self.assertNotIn("path", clips[0].to_public_dict())

    def test_unknown_clip_id_is_rejected(self) -> None:
        with self.assertRaises(DemoClipNotFound):
            self.catalog.get_clip("not-registered")

    def test_relative_media_root_is_rejected(self) -> None:
        with self.assertRaisesRegex(DemoCatalogError, "must be absolute"):
            DemoClipCatalog(Path("relative-media-root")).list_clips()

    def test_absolute_and_traversal_paths_are_rejected(self) -> None:
        for relative_path in (
            "C:\\private\\video.mp4",
            "\\\\server\\share\\video.mp4",
            "/private/video.mp4",
            "../outside.mp4",
            "fight/../../outside.mp4",
        ):
            with self.subTest(relative_path=relative_path):
                self.manifest["clips"][0]["relative_path"] = relative_path
                self._write_manifest()
                with self.assertRaises(DemoCatalogError):
                    self.catalog.list_clips()

    def test_missing_registered_file_is_reported(self) -> None:
        self.manifest["clips"][0]["relative_path"] = "fight/missing.mp4"
        self._write_manifest()

        with self.assertRaisesRegex(DemoCatalogError, "unavailable"):
            self.catalog.list_clips()

    def test_duplicate_clip_ids_are_rejected(self) -> None:
        self.manifest["clips"].append(dict(self.manifest["clips"][0]))
        self._write_manifest()

        with self.assertRaisesRegex(DemoCatalogError, "duplicate"):
            self.catalog.list_clips()

    def test_unsupported_manifest_version_is_rejected(self) -> None:
        self.manifest["schema_version"] = "2"
        self._write_manifest()

        with self.assertRaisesRegex(DemoCatalogError, "schema version"):
            self.catalog.list_clips()


if __name__ == "__main__":
    unittest.main()
