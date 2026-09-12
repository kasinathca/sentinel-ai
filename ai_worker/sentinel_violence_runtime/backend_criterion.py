"""Deterministic backend-side violence event criterion.

This module does NOT create/persist domain events. It only evaluates the frozen
3-of-5 criterion over worker model scores. Event duplicate/cooldown policy and
persistence remain application-domain responsibilities.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import math

from .constants import (
    LIVE_M_HISTORY,
    LIVE_N_REQUIRED,
    LIVE_SCORE_THRESHOLD,
)


@dataclass(frozen=True)
class CriterionState:
    camera_id: str
    score: float
    score_positive: bool
    history_count: int
    positive_count: int
    complete_history: bool
    qualified: bool
    threshold: float
    n_required: int
    m_history: int


class RollingViolenceCriterion:
    def __init__(
        self,
        *,
        threshold: float = LIVE_SCORE_THRESHOLD,
        n_required: int = LIVE_N_REQUIRED,
        m_history: int = LIVE_M_HISTORY,
    ) -> None:
        if not 0.0 <= threshold <= 1.0:
            raise ValueError("threshold must be within [0,1]")
        if m_history < 1:
            raise ValueError("m_history must be >= 1")
        if n_required < 1 or n_required > m_history:
            raise ValueError("n_required must satisfy 1 <= n_required <= m_history")

        self.threshold = float(threshold)
        self.n_required = int(n_required)
        self.m_history = int(m_history)
        self._history: dict[str, deque[bool]] = {}

    def observe(self, *, camera_id: str, score: float) -> CriterionState:
        if not isinstance(camera_id, str) or not camera_id.strip():
            raise ValueError("camera_id must be a non-empty string")

        score = float(score)
        if not math.isfinite(score) or not 0.0 <= score <= 1.0:
            raise ValueError("score must be finite and within [0,1]")

        history = self._history.setdefault(
            camera_id,
            deque(maxlen=self.m_history),
        )

        positive = score >= self.threshold
        history.append(positive)

        positive_count = sum(history)
        complete = len(history) == self.m_history
        qualified = complete and positive_count >= self.n_required

        return CriterionState(
            camera_id=camera_id,
            score=score,
            score_positive=positive,
            history_count=len(history),
            positive_count=int(positive_count),
            complete_history=complete,
            qualified=qualified,
            threshold=self.threshold,
            n_required=self.n_required,
            m_history=self.m_history,
        )

    def reset(self, camera_id: str) -> None:
        self._history.pop(camera_id, None)

    def reset_all(self) -> None:
        self._history.clear()
