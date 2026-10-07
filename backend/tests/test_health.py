from __future__ import annotations

import unittest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool

import app.health.router as health_router_module
from app.db.base import Base
from app.db import models  # noqa: F401 -- register mapped tables on Base.metadata
from app.db.readiness import EXPECTED_ALEMBIC_HEAD
from app.main import create_app


class HealthTests(unittest.TestCase):
    def test_liveness_is_independent_of_database_initialization(self):
        response = TestClient(create_app()).get("/api/v1/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["service"], "sentinel-api")
        self.assertEqual(response.json()["data"]["status"], "ok")

    def _client_with_engine(self, engine):
        app = create_app()
        app.dependency_overrides[health_router_module.get_readiness_engine] = lambda: engine
        return app, TestClient(app)

    def test_readiness_reports_uninitialized_database_without_stack_trace(self):
        engine = create_engine(
            "sqlite+pysqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        try:
            app, client = self._client_with_engine(engine)
            response = client.get("/api/v1/health/readiness")
            self.assertEqual(response.status_code, 503)
            body = response.json()["data"]
            self.assertEqual(body["status"], "not_ready")
            self.assertEqual(body["components"]["database"], "ok")
            self.assertEqual(body["components"]["database_schema"], "missing")
            self.assertIn("cameras", body["database"]["missing_tables"])
            self.assertNotIn("sqlite", body["database"]["message"].lower())
            app.dependency_overrides.clear()
        finally:
            engine.dispose()

    def test_readiness_passes_for_expected_schema_and_revision(self):
        engine = create_engine(
            "sqlite+pysqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        try:
            Base.metadata.create_all(engine)
            with engine.begin() as connection:
                connection.execute(
                    text("CREATE TABLE alembic_version (version_num VARCHAR(32) NOT NULL)")
                )
                connection.execute(
                    text("INSERT INTO alembic_version(version_num) VALUES (:revision)"),
                    {"revision": EXPECTED_ALEMBIC_HEAD},
                )

            app, client = self._client_with_engine(engine)
            response = client.get("/api/v1/health/readiness")
            self.assertEqual(response.status_code, 200)
            body = response.json()["data"]
            self.assertEqual(body["status"], "ready")
            self.assertEqual(body["components"]["database_schema"], "present")
            self.assertEqual(body["components"]["database_migration"], "current")
            self.assertEqual(
                body["database"]["current_revision"], EXPECTED_ALEMBIC_HEAD
            )
            app.dependency_overrides.clear()
        finally:
            engine.dispose()


if __name__ == "__main__":
    unittest.main()
