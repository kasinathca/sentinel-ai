from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from app.db.session import build_engine, ensure_database_parent


class SQLiteBootstrapTests(unittest.TestCase):
    def test_missing_parent_directory_is_created(self):
        with tempfile.TemporaryDirectory() as td:
            database_path = Path(td) / "nested" / "runtime" / "sentinel.db"
            url = "sqlite+pysqlite:///" + database_path.as_posix()

            self.assertFalse(database_path.parent.exists())

            ensure_database_parent(url)

            self.assertTrue(database_path.parent.exists())

            engine = build_engine(url)
            try:
                with engine.connect() as connection:
                    value = connection.exec_driver_sql("SELECT 1").scalar_one()
                    self.assertEqual(value, 1)
            finally:
                engine.dispose()

            self.assertTrue(database_path.exists())


if __name__ == "__main__":
    unittest.main()
