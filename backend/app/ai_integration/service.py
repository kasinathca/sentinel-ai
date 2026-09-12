from __future__ import annotations

from typing import Any

from pydantic import TypeAdapter, ValidationError

from app.events.violence_conditions import (
    ViolenceConditionConsumer,
    ViolenceConditionEvaluation,
)

from .criterion import (
    OutOfOrderObservationError,
    RollingViolenceCriterionEngine,
    StreamKey,
)
from .errors import (
    ModelContractMismatchError,
    OutOfOrderWorkerObservation,
    UnknownModelError,
    WorkerContractValidationError,
    WorkerReportedFailure,
)
from .model_registry import FrozenModelRegistry, ModelRegistry, UnknownModelVersionError
from .schemas import ViolenceWorkerFailure, WorkerViolenceResult


_RESULT_ADAPTER = TypeAdapter(WorkerViolenceResult)


class ViolenceWorkerResultService:
    def __init__(
        self,
        *,
        condition_consumer: ViolenceConditionConsumer,
        model_registry: ModelRegistry | None = None,
        criterion_engine: RollingViolenceCriterionEngine | None = None,
    ) -> None:
        self.condition_consumer = condition_consumer
        self.model_registry = model_registry or FrozenModelRegistry()
        self.criterion_engine = criterion_engine or RollingViolenceCriterionEngine()

    def consume_payload(self, payload: Any) -> ViolenceConditionEvaluation:
        try:
            result = _RESULT_ADAPTER.validate_python(payload)
        except ValidationError as exc:
            raise WorkerContractValidationError(str(exc)) from exc

        if isinstance(result, ViolenceWorkerFailure):
            # A valid worker failure is not a valid negative observation and must
            # not update the rolling violence criterion.
            raise WorkerReportedFailure(
                worker_code=result.error.code,
                message=result.error.message,
            )

        try:
            model_version = self.model_registry.get_violence_model_version(
                result.model.model_version_id
            )
        except UnknownModelVersionError as exc:
            raise UnknownModelError(str(result.model.model_version_id)) from exc

        if result.model.task != model_version.task:
            raise ModelContractMismatchError(
                "worker task does not match selected model metadata"
            )
        if result.result.score_semantics != model_version.score_semantics:
            raise ModelContractMismatchError(
                "worker score semantics do not match selected model metadata"
            )

        key = StreamKey(
            camera_id=result.camera_id,
            model_version_id=result.model.model_version_id,
        )

        try:
            criterion = self.criterion_engine.observe(
                key=key,
                score=result.result.score,
                window_started_at=result.window.started_at,
                threshold=model_version.event_threshold_value,
                n_required=model_version.n_required,
                m_history=model_version.history_window_size,
            )
        except OutOfOrderObservationError as exc:
            raise OutOfOrderWorkerObservation(str(exc)) from exc

        evaluation = ViolenceConditionEvaluation(
            camera_id=result.camera_id,
            model_version_id=result.model.model_version_id,
            job_id=result.job_id,
            correlation_id=result.correlation_id,
            window_started_at=result.window.started_at,
            window_ended_at=result.window.ended_at,
            score=result.result.score,
            score_positive=criterion.score_positive,
            history_count=criterion.history_count,
            positive_count=criterion.positive_count,
            complete_history=criterion.complete_history,
            candidate_condition=criterion.candidate_condition,
            threshold_snapshot=model_version.event_threshold_value,
            n_required_snapshot=model_version.n_required,
            m_history_snapshot=model_version.history_window_size,
            score_semantics=model_version.score_semantics,
        )

        self.condition_consumer.consume(evaluation)
        return evaluation
