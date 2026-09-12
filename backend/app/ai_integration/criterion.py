from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from datetime import datetime
import math
from uuid import UUID


@dataclass(frozen=True)
class StreamKey:
    camera_id: UUID
    model_version_id: UUID


@dataclass
class _StreamState:
    flags: deque[bool]
    last_started_at: datetime | None = None


@dataclass(frozen=True)
class CriterionEvaluation:
    score_positive: bool
    history_count: int
    positive_count: int
    complete_history: bool
    candidate_condition: bool


class OutOfOrderObservationError(ValueError):
    pass


class RollingViolenceCriterionEngine:
    """Frozen N-of-M violence criterion state, scoped per camera/model stream."""

    def __init__(self) -> None:
        self._states: dict[StreamKey, _StreamState] = {}

    def observe(
        self,
        *,
        key: StreamKey,
        score: float,
        window_started_at: datetime,
        threshold: float,
        n_required: int,
        m_history: int,
    ) -> CriterionEvaluation:
        score = float(score)

        if not math.isfinite(score) or not 0.0 <= score <= 1.0:
            raise ValueError("score must be finite and within [0,1]")
        if not 0.0 <= threshold <= 1.0:
            raise ValueError("threshold must be within [0,1]")
        if m_history < 1 or n_required < 1 or n_required > m_history:
            raise ValueError("invalid N-of-M violence criterion")

        state = self._states.get(key)
        if state is None:
            state = _StreamState(flags=deque(maxlen=m_history))
            self._states[key] = state
        elif state.flags.maxlen != m_history:
            raise ValueError("policy history size changed for an active stream")

        if (
            state.last_started_at is not None
            and window_started_at < state.last_started_at
        ):
            raise OutOfOrderObservationError(
                "violence observation is older than the latest accepted window"
            )

        score_positive = score >= threshold
        state.flags.append(score_positive)
        state.last_started_at = window_started_at

        positive_count = int(sum(state.flags))
        complete_history = len(state.flags) == m_history

        return CriterionEvaluation(
            score_positive=score_positive,
            history_count=len(state.flags),
            positive_count=positive_count,
            complete_history=complete_history,
            candidate_condition=(
                complete_history and positive_count >= n_required
            ),
        )

    def reset_stream(self, key: StreamKey) -> None:
        self._states.pop(key, None)

    def reset_all(self) -> None:
        self._states.clear()
