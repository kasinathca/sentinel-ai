from __future__ import annotations

import unittest

from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool

from app.db.readiness import (
    EXPECTED_ALEMBIC_HEAD,
    REQUIRED_APPLICATION_TABLES,
    inspect_database_readiness,
)


class DatabaseReadinessTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(
            "sqlite+pysqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )

    def tearDown(self):
        self.engine.dispose()

    def test_uninitialized_database_is_not_ready(self):
        state = inspect_database_readiness(self.engine)
        self.assertFalse(state.ready)
        self.assertEqual(state.connection, "ok")
        self.assertEqual(state.schema, "missing")
        self.assertIn("cameras", state.missing_tables)

    def test_tables_without_alembic_marker_are_not_ready(self):
        with self.engine.begin() as connection:
            for table in sorted(REQUIRED_APPLICATION_TABLES):
                connection.exec_driver_sql(
                    f'CREATE TABLE "{table}" (id INTEGER PRIMARY KEY)'
                )

        state = inspect_database_readiness(self.engine)
        self.assertFalse(state.ready)
        self.assertEqual(state.schema, "present")
        self.assertEqual(state.migration, "missing")

    def test_outdated_revision_is_not_ready(self):
        with self.engine.begin() as connection:
            for table in sorted(REQUIRED_APPLICATION_TABLES):
                connection.exec_driver_sql(
                    f'CREATE TABLE "{table}" (id INTEGER PRIMARY KEY)'
                )
            connection.exec_driver_sql(
                "CREATE TABLE alembic_version (version_num VARCHAR(32) NOT NULL)"
            )
            connection.execute(
                text("INSERT INTO alembic_version(version_num) VALUES ('old')")
            )

        state = inspect_database_readiness(self.engine)
        self.assertFalse(state.ready)
        self.assertEqual(state.migration, "outdated")
        self.assertEqual(state.current_revision, "old")

    def test_expected_revision_is_ready(self):
        with self.engine.begin() as connection:
            for table in sorted(REQUIRED_APPLICATION_TABLES):
                connection.exec_driver_sql(
                    f'CREATE TABLE "{table}" (id INTEGER PRIMARY KEY)'
                )
            connection.exec_driver_sql(
                "CREATE TABLE alembic_version (version_num VARCHAR(32) NOT NULL)"
            )
            connection.execute(
                text("INSERT INTO alembic_version(version_num) VALUES (:revision)"),
                {"revision": EXPECTED_ALEMBIC_HEAD},
            )

        state = inspect_database_readiness(self.engine)
        self.assertTrue(state.ready)
        self.assertEqual(state.migration, "current")
        self.assertEqual(state.current_revision, EXPECTED_ALEMBIC_HEAD)


if __name__ == "__main__":
    unittest.main()
