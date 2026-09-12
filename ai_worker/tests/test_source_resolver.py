from __future__ import annotations

import tempfile
from pathlib import Path
import unittest

from sentinel_violence_runtime.source_resolver import MappingSourceResolver
from sentinel_violence_runtime.errors import UnsupportedInputError


class SourceResolverTests(unittest.TestCase):
    def test_resolves_only_configured_reference(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            video = root / "video.mp4"
            video.write_bytes(b"demo")

            resolver = MappingSourceResolver(
                {"demo:video": "video.mp4"},
                mapping_base=root,
            )

            self.assertEqual(
                resolver.resolve("demo:video"),
                video.resolve(),
            )

            with self.assertRaises(UnsupportedInputError):
                resolver.resolve("../../arbitrary")


if __name__ == "__main__":
    unittest.main()
