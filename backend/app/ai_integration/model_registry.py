from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from .constants import (
    LIVE_M_HISTORY,
    LIVE_N_REQUIRED,
    LIVE_STRIDE_FEATURE_STEPS,
    LIVE_THRESHOLD,
    LIVE_WINDOW_FEATURE_STEPS,
    MODEL_CHECKPOINT_SHA256,
    MODEL_EXPERIMENT_ID,
    MODEL_VERSION_ID,
    MODEL_VERSION_LABEL,
    SCORE_SEMANTICS,
    VIOLENCE_TASK,
)


@dataclass(frozen=True)
class ViolenceModelVersion:
    id: UUID
    experiment_id: str
    version_label: str
    task: str
    checkpoint_sha256: str
    score_semantics: str
    event_threshold_value: float
    n_required: int
    history_window_size: int
    stride_feature_steps: int
    window_feature_steps: int


class UnknownModelVersionError(ValueError):
    pass


class ModelRegistry:
    def get_violence_model_version(
        self,
        model_version_id: UUID,
    ) -> ViolenceModelVersion:
        raise NotImplementedError


class FrozenModelRegistry(ModelRegistry):
    """Phase 2L in-memory model registry adapter.

    Persistence is intentionally deferred until the model registry database
    tables/migrations are baselined. This adapter contains only the frozen
    violence model identity and policy already documented in the repository.
    """

    def __init__(self) -> None:
        selected = ViolenceModelVersion(
            id=UUID(MODEL_VERSION_ID),
            experiment_id=MODEL_EXPERIMENT_ID,
            version_label=MODEL_VERSION_LABEL,
            task=VIOLENCE_TASK,
            checkpoint_sha256=MODEL_CHECKPOINT_SHA256,
            score_semantics=SCORE_SEMANTICS,
            event_threshold_value=LIVE_THRESHOLD,
            n_required=LIVE_N_REQUIRED,
            history_window_size=LIVE_M_HISTORY,
            stride_feature_steps=LIVE_STRIDE_FEATURE_STEPS,
            window_feature_steps=LIVE_WINDOW_FEATURE_STEPS,
        )
        self._by_id = {selected.id: selected}

    def get_violence_model_version(
        self,
        model_version_id: UUID,
    ) -> ViolenceModelVersion:
        try:
            return self._by_id[model_version_id]
        except KeyError as exc:
            raise UnknownModelVersionError(str(model_version_id)) from exc
