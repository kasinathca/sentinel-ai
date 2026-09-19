from __future__ import annotations

from fastapi import APIRouter, HTTPException

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
from app.events.persistence import (
    ViolenceEventPersistenceError,
    ViolenceEventPersistenceService,
)
from app.events.violence_conditions import (
    ViolenceConditionEvaluation,
    ViolenceConditionConsumer,
)


router = APIRouter(
    prefix="/api/v1/ai",
    tags=["ai"],
)


class DatabaseViolenceConditionConsumer(ViolenceConditionConsumer):
    """
    Receives a violence condition evaluation.

    Only a qualifying 3-of-5 condition is persisted.
    """

    def __init__(self) -> None:
        self.persistence = ViolenceEventPersistenceService(
            get_session_factory()
        )

    def consume(self, evaluation: ViolenceConditionEvaluation) -> None:
        if not evaluation.candidate_condition:
            return

        self.persistence.create_from_qualified_condition(
            evaluation=evaluation,
            requires_attention=True,
        )


_condition_consumer = DatabaseViolenceConditionConsumer()


_model_registry = DatabaseModelRegistry(
    get_session_factory()
)


_worker_service = ViolenceWorkerResultService(
    condition_consumer=_condition_consumer,
    model_registry=_model_registry,
)


@router.post("/violence/results")
def consume_violence_result(payload: dict):
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

    except ViolenceEventPersistenceError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
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
        }
    }