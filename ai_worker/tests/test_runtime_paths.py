from __future__ import annotations

import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from sentinel_violence_runtime.paths import (
    ENV_CHECKPOINT,
    ENV_EXTRACTOR_PYTHON,
    ENV_PROJECT_ROOT,
    resolve_project_root,
    resolve_runtime_paths,
)


class RuntimePathTests(unittest.TestCase):
    def test_project_root_can_come_from_environment(self):
        with tempfile.TemporaryDirectory() as td:
            with patch.dict(os.environ, {ENV_PROJECT_ROOT: td}, clear=False):
                self.assertEqual(resolve_project_root(), Path(td).resolve())

    def test_missing_root_is_explicit_failure(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                resolve_project_root()

    def test_artifact_override_can_be_relative_to_workspace(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            with patch.dict(
                os.environ,
                {ENV_CHECKPOINT: "custom/model.pt"},
                clear=False,
            ):
                paths = resolve_runtime_paths(root)
                self.assertEqual(paths.checkpoint, (root / "custom/model.pt").resolve())

    def test_extractor_python_override_removes_platform_layout_dependency(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            custom = root / "tools" / "python-custom"
            with patch.dict(
                os.environ,
                {ENV_EXTRACTOR_PYTHON: str(custom)},
                clear=False,
            ):
                paths = resolve_runtime_paths(root)
                self.assertEqual(paths.extractor_python, custom.resolve())


if __name__ == "__main__":
    unittest.main()
