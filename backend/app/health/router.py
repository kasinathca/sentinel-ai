from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status

from app.core.config import SETTINGS
from app.db.readiness import inspect_database_readiness
from app.db.session import get_engine


router = APIRouter(prefix="/api/v1", tags=["health"])


def get_readiness_engine():
    """Dependency seam used by readiness tests without changing app DB state."""
    return get_engine()


@router.get("/health")
def health() -> dict:
    """Process liveness only; intentionally does not claim DB readiness."""
    return {
        "data": {
            "status": "ok",
            "service": SETTINGS.service_name,
            "version": SETTINGS.service_version,
        }
    }


@router.get("/health/readiness")
def readiness(
    response: Response,
    engine=Depends(get_readiness_engine),
) -> dict:
    """Report whether the integrated backend database is usable.

    The route implements the readiness path already proposed by the API
    specification. It remains a deployment/integration contract until the team
    formally baselines it.
    """
    database = inspect_database_readiness(engine)

    if not database.ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return {
        "data": {
            "status": "ready" if database.ready else "not_ready",
            "components": {
                "database": database.connection,
                "database_schema": database.schema,
                "database_migration": database.migration,
                # These subsystems are deliberately not fabricated here. Their
                # readiness contracts remain separate/unimplemented.
                "ai_worker": "not_checked",
                "evidence_storage": "not_integrated",
            },
            "database": database.to_public_dict(),
        }
    }
