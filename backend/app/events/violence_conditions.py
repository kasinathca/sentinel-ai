from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True)
class ViolenceConditionEvaluation:
    camera_id: UUID
    model_version_id: UUID
    job_id: UUID
    correlation_id: UUID
    window_started_at: datetime
    window_ended_at: datetime
    score: float
    score_positive: bool
    history_count: int
    positive_count: int
    complete_history: bool
    candidate_condition: bool
    threshold_snapshot: float
    n_required_snapshot: int
    m_history_snapshot: int
    score_semantics: str


class ViolenceConditionConsumer(Protocol):
    """Port from AI integration into the event domain.

    A candidate condition is not the same thing as a newly persisted event.
    Duplicate/cooldown/retrigger and persistence semantics remain owned by the
    event domain.
    """

    def consume(self, evaluation: ViolenceConditionEvaluation) -> None:
        ...


class RecordingViolenceConditionConsumer:
    """Development/test adapter that records all accepted evaluations."""

    def __init__(self) -> None:
        self.evaluations: list[ViolenceConditionEvaluation] = []

    def consume(self, evaluation: ViolenceConditionEvaluation) -> None:
        self.evaluations.append(evaluation)
