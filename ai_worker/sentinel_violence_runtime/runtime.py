"""Transport-neutral Sentinel violence AI-worker runtime core."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
import tempfile
from typing import Any

import numpy as np

from .constants import (
    CHECKPOINT_RELATIVE,
    EXACT_EXTRACTOR_PYTHON_RELATIVE,
    EXACT_EXTRACTOR_WORKER_RELATIVE,
    MODEL_VERSION_ID,
    MODEL_VERSION_LABEL,
    SCHEMA_VERSION,
    SCORE_LABEL,
    SCORE_SEMANTICS,
    SOURCE_FRAMES_PER_FEATURE_STEP,
    TASK_VIOLENCE,
    TRAIN_SCRIPT_RELATIVE,
)
from .contracts import (
    WorkerProcessingRequest,
    ViolenceWindowResult,
    WorkerFailureResult,
)
from .errors import (
    INTERNAL_WORKER_ERROR,
    SentinelWorkerError,
    UnsupportedInputError,
)
from .extractor_client import PersistentExactExtractor
from .media_probe import probe_media
from .temporal_model import FrozenTemporalScorer
from .time_utils import (
    feature_window_timestamps,
    parse_utc_timestamp,
)


@dataclass(frozen=True)
class RuntimeHealth:
    state: str
    process_alive: bool
    extractor_ready: bool
    temporal_model_ready: bool
    model_version_id: str
    task: str
    detail: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "state": self.state,
            "process_alive": self.process_alive,
            "extractor_ready": self.extractor_ready,
            "temporal_model_ready": self.temporal_model_ready,
            "model_version_id": self.model_version_id,
            "task": self.task,
            "detail": self.detail,
        }


class ViolenceRuntime:
    def __init__(
        self,
        *,
        project_root: Path,
        work_dir: Path | None = None,
        ffprobe: str = "ffprobe",
        temporal_batch_size: int = 64,
    ) -> None:
        self.project_root = project_root.resolve()
        self.work_dir = (
            work_dir.resolve()
            if work_dir is not None
            else (
                self.project_root
                / "sentinel_runtime_validation"
                / "runtime_work"
            )
        )
        self.ffprobe = ffprobe

        self._extractor = PersistentExactExtractor(
            python_exe=self.project_root / EXACT_EXTRACTOR_PYTHON_RELATIVE,
            worker_script=self.project_root / EXACT_EXTRACTOR_WORKER_RELATIVE,
            project_root=self.project_root,
            stderr_log=(
                self.work_dir
                / "logs"
                / "exact_extractor.stderr.log"
            ),
        )

        self._scorer = FrozenTemporalScorer(
            training_script=self.project_root / TRAIN_SCRIPT_RELATIVE,
            checkpoint=self.project_root / CHECKPOINT_RELATIVE,
            batch_size=temporal_batch_size,
        )

        self._started = False
        self._last_error: str | None = None

    def start(self) -> None:
        if self._started:
            return

        self.work_dir.mkdir(parents=True, exist_ok=True)

        try:
            self._scorer.load()
            self._extractor.start()
        except Exception as exc:
            self._last_error = str(exc)
            self._extractor.close(force=True)
            raise

        self._started = True
        self._last_error = None

    def close(self) -> None:
        self._extractor.close()
        self._started = False

    def health(self) -> RuntimeHealth:
        extractor_ready = self._extractor.is_ready
        model_ready = self._scorer.is_ready

        if extractor_ready and model_ready:
            state = "ready"
            detail = None
        elif self._last_error:
            state = "failed"
            detail = self._last_error
        elif extractor_ready or model_ready:
            state = "degraded"
            detail = "Only part of the violence runtime is ready."
        else:
            state = "starting" if not self._started else "failed"
            detail = None

        return RuntimeHealth(
            state=state,
            process_alive=True,
            extractor_ready=extractor_ready,
            temporal_model_ready=model_ready,
            model_version_id=MODEL_VERSION_ID,
            task=TASK_VIOLENCE,
            detail=detail,
        )

    def capabilities(self) -> dict[str, Any]:
        return {
            "data": {
                "tasks": [TASK_VIOLENCE],
                "models": [
                    {
                        "task": TASK_VIOLENCE,
                        "model_version_id": MODEL_VERSION_ID,
                        "version_label": MODEL_VERSION_LABEL,
                    }
                ],
            }
        }

    def process_file(
        self,
        *,
        request: WorkerProcessingRequest,
        source_path: Path,
        source_started_at: str,
    ) -> list[ViolenceWindowResult] | WorkerFailureResult:
        """
        Process a controlled file source.

        source_started_at is supplied by the source adapter/application because
        the transport-neutral request schema does not define the media-origin
        absolute timestamp. The file adapter uses it only to anchor window times.
        """
        try:
            self.start()

            if request.source.source_kind != "file":
                raise ValueError("Only file sources are supported by this adapter.")

            source_path = source_path.resolve()
            if not source_path.exists() or not source_path.is_file():
                raise UnsupportedInputError(
                    "Resolved controlled source file is unavailable."
                )

            source_start_dt = parse_utc_timestamp(source_started_at)
            media = probe_media(source_path, ffprobe=self.ffprobe)

            source_key = hashlib.sha256(
                (
                    request.job_id
                    + "|"
                    + str(source_path)
                ).encode("utf-8")
            ).hexdigest()[:24]

            feature_path = (
                self.work_dir
                / "features"
                / f"{source_key}.npy"
            )

            self._extractor.extract(
                video_path=source_path,
                output_path=feature_path,
            )

            features = np.asarray(
                np.load(feature_path),
                dtype=np.float32,
            )

            scores = self._scorer.score_feature_array(features)

            if len(scores) != features.shape[0]:
                raise RuntimeError("Temporal score count does not match I3D features.")

            results: list[ViolenceWindowResult] = []

            for index, score in enumerate(scores):
                started_at, ended_at = feature_window_timestamps(
                    source_started_at=source_start_dt,
                    feature_index=index,
                    fps=media.fps,
                    duration_seconds=media.duration_seconds,
                    source_frames_per_feature_step=SOURCE_FRAMES_PER_FEATURE_STEP,
                )

                results.append(
                    ViolenceWindowResult(
                        schema_version=SCHEMA_VERSION,
                        job_id=request.job_id,
                        correlation_id=request.correlation_id,
                        camera_id=request.source.camera_id,
                        window_started_at=started_at,
                        window_ended_at=ended_at,
                        model_version_id=MODEL_VERSION_ID,
                        label=SCORE_LABEL,
                        score=float(score),
                        score_semantics=SCORE_SEMANTICS,
                    )
                )

            return results

        except SentinelWorkerError as exc:
            self._last_error = exc.safe_message
            return WorkerFailureResult(
                schema_version=SCHEMA_VERSION,
                job_id=request.job_id,
                correlation_id=request.correlation_id,
                camera_id=request.source.camera_id,
                code=exc.code,
                message=exc.safe_message,
            )
        except Exception:
            self._last_error = "Unhandled violence runtime failure."
            return WorkerFailureResult(
                schema_version=SCHEMA_VERSION,
                job_id=request.job_id,
                correlation_id=request.correlation_id,
                camera_id=request.source.camera_id,
                code=INTERNAL_WORKER_ERROR,
                message="Internal violence worker error.",
            )

    def __enter__(self) -> "ViolenceRuntime":
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        self.close()
        return False
