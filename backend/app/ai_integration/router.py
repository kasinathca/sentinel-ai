from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from app.ai_integration.database_model_registry import DatabaseModelRegistry
from app.ai_integration.errors import (
    ModelContractMismatchError,
    OutOfOrderWorkerObservation,
    UnknownModelError,
    WorkerContractValidationError,
    WorkerReportedFailure,
)
from app.ai_integration.service import ViolenceWorkerResultService
from app.db.session import get_session_factory
from app.db.models import Camera
from app.events.violence_conditions import (
    ViolenceConditionEvaluation,
    ViolenceConditionConsumer,
)
from app.ai_integration.schemas import WorkerViolenceResult


router = APIRouter(
    prefix="/api/v1/ai",
    tags=["ai"],
)


def get_db():
    session_factory = get_session_factory()
    with session_factory() as session:
        yield session


class DatabaseViolenceConditionConsumer(ViolenceConditionConsumer):
    """
    Receives a violence condition evaluation.

    The frozen criterion produces candidates. Event episode/deduplication
    semantics are unresolved, so this adapter intentionally does not persist.
    """

    def consume(self, evaluation: ViolenceConditionEvaluation) -> None:
        return None


_condition_consumer = DatabaseViolenceConditionConsumer()


_model_registry = DatabaseModelRegistry(
    get_session_factory()
)


_worker_service = ViolenceWorkerResultService(
    condition_consumer=_condition_consumer,
    model_registry=_model_registry,
)


@router.post("/violence/results")
def consume_violence_result(
    payload: WorkerViolenceResult,
    session: Session = Depends(get_db),
):
    if session.get(Camera, payload.camera_id) is None:
        raise HTTPException(status_code=404, detail="Camera was not found.")
    try:
        evaluation = _worker_service.consume_payload(payload)

    except WorkerContractValidationError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except UnknownModelError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except ModelContractMismatchError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except OutOfOrderWorkerObservation as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc

    except WorkerReportedFailure as exc:
        raise HTTPException(
            status_code=422,
            detail={
                "code": exc.worker_code,
                "message": exc.message,
            },
        ) from exc

    return {
        "data": {
            "camera_id": str(evaluation.camera_id),
            "model_version_id": str(evaluation.model_version_id),
            "job_id": str(evaluation.job_id),
            "correlation_id": str(evaluation.correlation_id),
            "score": evaluation.score,
            "score_positive": evaluation.score_positive,
            "history_count": evaluation.history_count,
            "positive_count": evaluation.positive_count,
            "complete_history": evaluation.complete_history,
            "candidate_condition": evaluation.candidate_condition,
            "threshold_snapshot": evaluation.threshold_snapshot,
            "n_required_snapshot": evaluation.n_required_snapshot,
            "m_history_snapshot": evaluation.m_history_snapshot,
            "score_semantics": evaluation.score_semantics,
            "event_persisted": False,
            "event_lifecycle": (
                "awaiting_domain_policy"
                if evaluation.candidate_condition
                else "not_qualified"
            ),
        }
    }
