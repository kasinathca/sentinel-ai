from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import Engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError


# Keep this synchronized with backend/alembic/versions/. A mismatch is an
# integration/setup defect, not a reason to auto-create tables at request time.
EXPECTED_ALEMBIC_HEAD = "20261005_0002"

# Tables required by the currently integrated staging backend routes and frozen
# violence-model registry. Future migrations should extend this set only when a
# newly required table becomes part of backend readiness.
REQUIRED_APPLICATION_TABLES = frozenset(
    {
        "cameras",
        "models",
        "model_versions",
        "violence_event_policies",
        "events",
        "violence_event_context",
    }
)


@dataclass(frozen=True)
class DatabaseReadiness:
    ready: bool
    connection: str
    schema: str
    migration: str
    current_revision: str | None
    expected_revision: str
    missing_tables: tuple[str, ...]
    message: str

    def to_public_dict(self) -> dict:
        """Return a safe response payload without DB URLs or raw exceptions."""
        return {
            "ready": self.ready,
            "connection": self.connection,
            "schema": self.schema,
            "migration": self.migration,
            "current_revision": self.current_revision,
            "expected_revision": self.expected_revision,
            "missing_tables": list(self.missing_tables),
            "message": self.message,
        }


def inspect_database_readiness(engine: Engine) -> DatabaseReadiness:
    """Check connectivity, required tables, and the expected Alembic revision.

    This function is intentionally read-only. It never runs migrations and never
    creates tables. Schema changes remain an explicit deployment/setup action.
    """

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            inspector = inspect(connection)
            tables = set(inspector.get_table_names())

            missing_tables = tuple(sorted(REQUIRED_APPLICATION_TABLES - tables))
            if missing_tables:
                return DatabaseReadiness(
                    ready=False,
                    connection="ok",
                    schema="missing",
                    migration="unknown",
                    current_revision=None,
                    expected_revision=EXPECTED_ALEMBIC_HEAD,
                    missing_tables=missing_tables,
                    message=(
                        "Database is reachable but the Sentinel schema is not "
                        "initialized. Run backend/scripts/init_database.py."
                    ),
                )

            if "alembic_version" not in tables:
                return DatabaseReadiness(
                    ready=False,
                    connection="ok",
                    schema="present",
                    migration="missing",
                    current_revision=None,
                    expected_revision=EXPECTED_ALEMBIC_HEAD,
                    missing_tables=(),
                    message=(
                        "Sentinel tables exist but the Alembic revision marker is "
                        "missing. Run the documented database initialization."
                    ),
                )

            current_revision = connection.execute(
                text("SELECT version_num FROM alembic_version")
            ).scalar_one_or_none()

            if current_revision != EXPECTED_ALEMBIC_HEAD:
                return DatabaseReadiness(
                    ready=False,
                    connection="ok",
                    schema="present",
                    migration="outdated",
                    current_revision=current_revision,
                    expected_revision=EXPECTED_ALEMBIC_HEAD,
                    missing_tables=(),
                    message=(
                        "Database migration revision is not at the integrated "
                        "backend head. Run backend/scripts/init_database.py."
                    ),
                )

            return DatabaseReadiness(
                ready=True,
                connection="ok",
                schema="present",
                migration="current",
                current_revision=current_revision,
                expected_revision=EXPECTED_ALEMBIC_HEAD,
                missing_tables=(),
                message="Database is initialized and at the expected migration head.",
            )

    except SQLAlchemyError:
        return DatabaseReadiness(
            ready=False,
            connection="unavailable",
            schema="unknown",
            migration="unknown",
            current_revision=None,
            expected_revision=EXPECTED_ALEMBIC_HEAD,
            missing_tables=(),
            message="Database connection/readiness check failed.",
        )
