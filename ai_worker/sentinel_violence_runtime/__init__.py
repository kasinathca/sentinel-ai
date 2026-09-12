"""Sentinel AI frozen violence runtime integration package.

Transport-neutral core for the qualified EXP-VIO-TEMPORAL-001 model and the
validation-selected live event criterion.

The AI worker emits model observations/scores. Domain event creation remains a
backend responsibility.
"""

from .constants import (
    MODEL_EXPERIMENT_ID,
    MODEL_VERSION_ID,
    MODEL_VERSION_LABEL,
    LIVE_SCORE_THRESHOLD,
    LIVE_N_REQUIRED,
    LIVE_M_HISTORY,
)
from .contracts import (
    WorkerProcessingRequest,
    ViolenceWindowResult,
    WorkerFailureResult,
)
from .backend_criterion import RollingViolenceCriterion, CriterionState

__all__ = [
    "MODEL_EXPERIMENT_ID",
    "MODEL_VERSION_ID",
    "MODEL_VERSION_LABEL",
    "LIVE_SCORE_THRESHOLD",
    "LIVE_N_REQUIRED",
    "LIVE_M_HISTORY",
    "WorkerProcessingRequest",
    "ViolenceWindowResult",
    "WorkerFailureResult",
    "RollingViolenceCriterion",
    "CriterionState",
]
