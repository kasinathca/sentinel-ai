from __future__ import annotations

import tempfile
from pathlib import Path
import unittest


class CliOutputDirectoryTests(unittest.TestCase):
    def test_nested_output_parent_can_be_created_before_open(self):
        with tempfile.TemporaryDirectory() as td:
            output = Path(td) / "nested" / "runtime_work" / "result.jsonl"

            self.assertFalse(output.parent.exists())

            output.parent.mkdir(parents=True, exist_ok=True)
            with output.open("w", encoding="utf-8") as handle:
                handle.write('{"ok":true}\n')

            self.assertTrue(output.exists())
            self.assertEqual(
                output.read_text(encoding="utf-8"),
                '{"ok":true}\n',
            )


if __name__ == "__main__":
    unittest.main()
