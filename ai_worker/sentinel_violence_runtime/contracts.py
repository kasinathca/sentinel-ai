"""Transport-neutral worker contracts matching docs/07-api-specification.md."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any
from uuid import UUID

from .constants import SCHEMA_VERSION, TASK_VIOLENCE
from .errors import InvalidRequestError
from .time_utils import parse_utc_timestamp


def _require_nonempty_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InvalidRequestError(f"{field} must be a non-empty string.")
    return value.strip()


def _require_uuid_string(value: Any, field: str) -> str:
    text = _require_nonempty_string(value, field)
    try:
        UUID(text)
    except ValueError as exc:
        raise InvalidRequestError(f"{field} must be a UUID string.") from exc
    return text


@dataclass(frozen=True)
class WorkerSource:
    camera_id: str
    source_kind: str
    source_locator_ref: str

    @classmethod
    def from_dict(cls, data: Any) -> "WorkerSource":
        if not isinstance(data, dict):
            raise InvalidRequestError("source must be an object.")

        camera_id = _require_uuid_string(data.get("camera_id"), "source.camera_id")
        source_kind = _require_nonempty_string(
            data.get("source_kind"), "source.source_kind"
        )
        source_locator_ref = _require_nonempty_string(
            data.get("source_locator_ref"), "source.source_locator_ref"
        )

        if source_kind != "file":
            raise InvalidRequestError(
                "This runtime adapter currently supports source_kind='file' only."
            )

        return cls(
            camera_id=camera_id,
            source_kind=source_kind,
            source_locator_ref=source_locator_ref,
        )


@dataclass(frozen=True)
class WorkerProcessingRequest:
    schema_version: str
    job_id: str
    correlation_id: str
    source: WorkerSource
    tasks: tuple[str, ...]
    requested_at: str
    options: dict[str, Any]

    @classmethod
    def from_dict(cls, data: Any) -> "WorkerProcessingRequest":
        if not isinstance(data, dict):
            raise InvalidRequestError("Worker request must be a JSON object.")

        schema_version = _require_nonempty_string(
            data.get("schema_version"), "schema_version"
        )
        if schema_version != SCHEMA_VERSION:
            raise InvalidRequestError(
                f"Unsupported schema_version {schema_version!r}; "
                f"expected {SCHEMA_VERSION!r}."
            )

        job_id = _require_uuid_string(data.get("job_id"), "job_id")
        correlation_id = _require_uuid_string(
            data.get("correlation_id"), "correlation_id"
        )
        source = WorkerSource.from_dict(data.get("source"))

        tasks_raw = data.get("tasks")
        if not isinstance(tasks_raw, list) or not tasks_raw:
            raise InvalidRequestError("tasks must be a non-empty array.")

        tasks = tuple(_require_nonempty_string(x, "tasks[]") for x in tasks_raw)
        if TASK_VIOLENCE not in tasks:
            raise InvalidRequestError(
                f"tasks must include {TASK_VIOLENCE!r} for this runtime."
            )

        unsupported = sorted(set(tasks) - {TASK_VIOLENCE})
        if unsupported:
            raise InvalidRequestError(
                "This violence-only runtime cannot execute additional tasks: "
                + ", ".join(unsupported)
            )

        requested_at = _require_nonempty_string(
            data.get("requested_at"), "requested_at"
        )
        parse_utc_timestamp(requested_at)

        options = data.get("options", {})
        if not isinstance(options, dict):
            raise InvalidRequestError("options must be an object.")

        return cls(
            schema_version=schema_version,
            job_id=job_id,
            correlation_id=correlation_id,
            source=source,
            tasks=tasks,
            requested_at=requested_at,
            options=dict(options),
        )


@dataclass(frozen=True)
class ViolenceWindowResult:
    schema_version: str
    job_id: str
    correlation_id: str
    camera_id: str
    window_started_at: str
    window_ended_at: str
    model_version_id: str
    label: str
    score: float
    score_semantics: str

    def __post_init__(self) -> None:
        _require_uuid_string(self.job_id, "job_id")
        _require_uuid_string(self.correlation_id, "correlation_id")
        _require_uuid_string(self.camera_id, "camera_id")
        _require_uuid_string(self.model_version_id, "model.model_version_id")

        parse_utc_timestamp(self.window_started_at)
        parse_utc_timestamp(self.window_ended_at)

        if self.schema_version != SCHEMA_VERSION:
            raise InvalidRequestError("Unexpected schema_version in result.")
        if not math.isfinite(float(self.score)):
            raise InvalidRequestError("result.score must be finite.")
        if not 0.0 <= float(self.score) <= 1.0:
            raise InvalidRequestError("result.score must be within [0, 1].")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "job_id": self.job_id,
            "correlation_id": self.correlation_id,
            "camera_id": self.camera_id,
            "window": {
                "started_at": self.window_started_at,
                "ended_at": self.window_ended_at,
            },
            "status": "success",
            "model": {
                "model_version_id": self.model_version_id,
                "task": TASK_VIOLENCE,
            },
            "result": {
                "label": self.label,
                "score": float(self.score),
                "score_semantics": self.score_semantics,
            },
        }


@dataclass(frozen=True)
class WorkerFailureResult:
    schema_version: str
    job_id: str
    correlation_id: str
    camera_id: str
    code: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "job_id": self.job_id,
            "correlation_id": self.correlation_id,
            "camera_id": self.camera_id,
            "status": "failed",
            "error": {
                "code": self.code,
                "message": self.message,
            },
        }
