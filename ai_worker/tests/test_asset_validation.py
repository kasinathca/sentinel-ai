import json
from pathlib import Path
import tempfile
import unittest

from sentinel_violence_runtime.asset_validation import (
    load_manifest,
    validate_files,
    validate_frozen_contract,
)


class QualifiedRuntimeAssetValidationTests(unittest.TestCase):
    def test_committed_manifest_matches_frozen_runtime_constants(self):
        manifest = load_manifest()
        self.assertEqual(validate_frozen_contract(manifest), [])

    def test_file_validation_detects_hash_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "asset.bin"
            target.write_bytes(b"wrong")
            manifest = {
                "files": [
                    {
                        "role": "test_asset",
                        "path": "asset.bin",
                        "size": 5,
                        "sha256": "0" * 64,
                    }
                ],
                "media": [],
            }
            errors = validate_files(root, manifest, include_media=True)
        self.assertEqual(len(errors), 1)
        self.assertIn("SHA256 mismatch", errors[0])

    def test_manifest_is_valid_json_and_contains_both_fixture_roles(self):
        manifest_path = Path(__file__).resolve().parents[1] / "qualified_runtime_assets.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        roles = {item["role"] for item in manifest["media"]}
        self.assertEqual(
            roles,
            {
                "approved_negative_normal_fixture",
                "approved_positive_fighting_fixture",
            },
        )


if __name__ == "__main__":
    unittest.main()
