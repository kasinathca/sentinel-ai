from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, model_validator

from .constants import ALLOWED_WORKER_ERROR_CODES, SCORE_SEMANTICS


class ContractModel(BaseModel):
    """Reject undocumented fields while parsing normal JSON scalar encodings."""

    model_config = ConfigDict(extra="forbid")


class WorkerWindow(ContractModel):
    started_at: datetime
    ended_at: datetime

    @model_validator(mode="after")
    def validate_window(self) -> "WorkerWindow":
        if self.started_at.tzinfo is None or self.ended_at.tzinfo is None:
            raise ValueError("worker window timestamps must contain a timezone")
        if self.ended_at <= self.started_at:
            raise ValueError("worker window ended_at must be after started_at")
        return self


class WorkerModelIdentity(ContractModel):
    model_version_id: UUID
    task: Literal["violence_fighting"]


class ViolenceScorePayload(ContractModel):
    label: Literal["fighting"]
    score: StrictFloat = Field(ge=0.0, le=1.0, allow_inf_nan=False)
    score_semantics: str

    @model_validator(mode="after")
    def validate_semantics(self) -> "ViolenceScorePayload":
        if self.score_semantics != SCORE_SEMANTICS:
            raise ValueError(
                "worker score_semantics does not match the frozen model contract"
            )
        return self


class ViolenceWorkerSuccess(ContractModel):
    schema_version: Literal["1"]
    job_id: UUID
    correlation_id: UUID
    camera_id: UUID
    window: WorkerWindow
    status: Literal["success"]
    model: WorkerModelIdentity
    result: ViolenceScorePayload


class WorkerErrorPayload(ContractModel):
    code: str
    message: str

    @model_validator(mode="after")
    def validate_error(self) -> "WorkerErrorPayload":
        if self.code not in ALLOWED_WORKER_ERROR_CODES:
            raise ValueError(f"unknown worker error code: {self.code}")
        if not self.message.strip():
            raise ValueError("worker error message must not be empty")
        return self


class ViolenceWorkerFailure(ContractModel):
    schema_version: Literal["1"]
    job_id: UUID
    correlation_id: UUID
    camera_id: UUID
    status: Literal["failed"]
    error: WorkerErrorPayload


WorkerViolenceResult = Annotated[
    Union[ViolenceWorkerSuccess, ViolenceWorkerFailure],
    Field(discriminator="status"),
]
