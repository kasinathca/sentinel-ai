"""Background bridge from the selected demo source to the frozen AI worker."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import threading
from typing import Callable
from uuid import UUID, uuid4

from app.ai_integration.constants import (
    LIVE_M_HISTORY,
    LIVE_N_REQUIRED,
    LIVE_THRESHOLD,
    MODEL_VERSION_ID,
    SCORE_SEMANTICS,
)
from app.ai_integration.service import ViolenceProcessingOutcome
from app.cameras.constants import DEMO_CAMERA_ID
from app.demo.clip_catalog import DemoClip


@dataclass(frozen=True)
class DemoAIStatus:
    state: str = "stopped"
    source_session_id: UUID | None = None
    latest_score: float | None = None
    candidate_condition: bool = False
    event_id: UUID | None = None
    processed_windows: int = 0
    error: str | None = None

    def to_public_dict(self) -> dict[str, object]:
        return {
            "state": self.state,
            "source_session_id": (
                str(self.source_session_id) if self.source_session_id else None
            ),
            "latest_score": self.latest_score,
            "candidate_condition": self.candidate_condition,
            "event_id": str(self.event_id) if self.event_id else None,
            "processed_windows": self.processed_windows,
            "error": self.error,
            "model_version_id": MODEL_VERSION_ID,
            "threshold": LIVE_THRESHOLD,
            "criterion": f"{LIVE_N_REQUIRED}-of-{LIVE_M_HISTORY}",
            "score_semantics": SCORE_SEMANTICS,
        }


class DemoAIOrchestrator:
    """Run real whole-file inference outside FastAPI's request thread.

    The worker CLI performs extraction and temporal inference in a separate
    process. Genuine window results are then released according to their media
    timestamps so a faster-than-real-time worker cannot publish future alerts
    at source start.
    """

    def __init__(
        self,
        result_consumer: Callable[[dict], ViolenceProcessingOutcome],
        *,
        worker_python: str | None = None,
    ) -> None:
        self._result_consumer = result_consumer
        self._worker_python = worker_python or os.environ.get(
            "SENTINEL_AI_PYTHON", "python"
        )
        self._lock = threading.RLock()
        self._stop_event = threading.Event()
        self._worker: threading.Thread | None = None
        self._process: subprocess.Popen[str] | None = None
        self._generation = 0
        self._status = DemoAIStatus()

    def start(self, clip: DemoClip, source_session_id: UUID) -> None:
        self.stop()
        with self._lock:
            self._generation += 1
            generation = self._generation
            self._stop_event.clear()
            self._status = DemoAIStatus(
                state="starting", source_session_id=source_session_id
            )
            self._worker = threading.Thread(
                target=self._run,
                args=(clip, source_session_id, generation),
                name="sentinel-demo-ai",
                daemon=True,
            )
            self._worker.start()

    def restart(self, clip: DemoClip, source_session_id: UUID) -> None:
        self.start(clip, source_session_id)

    def stop(self) -> None:
        self._stop_event.set()
        with self._lock:
            process = self._process
            worker = self._worker
            self._generation += 1
        if process is not None and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=3)
        if worker is not None and worker is not threading.current_thread():
            worker.join(timeout=5)
        with self._lock:
            self._process = None
            self._worker = None
            self._status = DemoAIStatus(state="stopped")

    def status(self) -> DemoAIStatus:
        with self._lock:
            return self._status

    def _run(self, clip: DemoClip, source_session_id: UUID, generation: int) -> None:
        started_at = datetime.now(timezone.utc)
        ai_root = Path(__file__).resolve().parents[3] / "ai_worker"
        python_exe = shutil.which(self._worker_python) or self._worker_python
        with tempfile.TemporaryDirectory(prefix="sentinel_ai_") as temp_name:
            temp = Path(temp_name)
            request_path = temp / "request.json"
            source_map_path = temp / "source-map.json"
            request_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1",
                        "job_id": str(uuid4()),
                        "correlation_id": str(source_session_id),
                        "source": {
                            "camera_id": str(DEMO_CAMERA_ID),
                            "source_kind": "file",
                            "source_locator_ref": clip.clip_id,
                        },
                        "tasks": ["violence_fighting"],
                        "requested_at": started_at.isoformat(),
                        "options": {},
                    }
                ),
                encoding="utf-8",
            )
            source_map_path.write_text(
                json.dumps({clip.clip_id: str(clip.resolved_path)}), encoding="utf-8"
            )
            environment = os.environ.copy()
            current_pythonpath = environment.get("PYTHONPATH", "")
            environment["PYTHONPATH"] = str(ai_root) + (
                os.pathsep + current_pythonpath if current_pythonpath else ""
            )
            command = [
                str(python_exe),
                "-m",
                "sentinel_violence_runtime.cli",
                "--source-map",
                str(source_map_path),
                "--request",
                str(request_path),
                "--source-started-at",
                started_at.isoformat(),
            ]
            try:
                process = subprocess.Popen(
                    command,
                    cwd=str(ai_root.parent),
                    env=environment,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding="utf-8",
                )
            except (OSError, ValueError):
                self._fail(generation, "The configured AI worker could not be started.")
                return
            with self._lock:
                if generation != self._generation:
                    process.terminate()
                    return
                self._process = process
                self._status = DemoAIStatus(
                    state="processing", source_session_id=source_session_id
                )

            assert process.stdout is not None
            try:
                for line in process.stdout:
                    if self._stop_event.is_set() or generation != self._generation:
                        process.terminate()
                        return
                    payload = json.loads(line)
                    if payload.get("status") == "failed":
                        self._fail(
                            generation,
                            payload.get("error", {}).get("message", "AI inference failed."),
                        )
                        return
                    ended_at = datetime.fromisoformat(
                        payload["window"]["ended_at"].replace("Z", "+00:00")
                    )
                    delay = (ended_at - datetime.now(timezone.utc)).total_seconds()
                    if delay > 0 and self._stop_event.wait(delay):
                        process.terminate()
                        return
                    outcome = self._result_consumer(payload)
                    self._accept_outcome(generation, source_session_id, outcome)
            except Exception:
                self._fail(generation, "AI inference result processing failed.")
                process.terminate()
                return
            return_code = process.wait()
            if return_code != 0:
                self._fail(generation, "The AI worker exited before completing inference.")
                return
            with self._lock:
                if generation == self._generation:
                    self._status = DemoAIStatus(
                        **{**self._status.__dict__, "state": "completed"}
                    )
                    self._process = None

    def _accept_outcome(
        self,
        generation: int,
        source_session_id: UUID,
        outcome: ViolenceProcessingOutcome,
    ) -> None:
        with self._lock:
            if generation != self._generation:
                return
            previous = self._status
            self._status = DemoAIStatus(
                state="processing",
                source_session_id=source_session_id,
                latest_score=outcome.evaluation.score,
                candidate_condition=outcome.evaluation.candidate_condition,
                event_id=outcome.event_id or previous.event_id,
                processed_windows=previous.processed_windows + 1,
            )

    def _fail(self, generation: int, message: str) -> None:
        with self._lock:
            if generation == self._generation:
                self._status = DemoAIStatus(
                    state="failed",
                    source_session_id=self._status.source_session_id,
                    latest_score=self._status.latest_score,
                    candidate_condition=self._status.candidate_condition,
                    event_id=self._status.event_id,
                    processed_windows=self._status.processed_windows,
                    error=message,
                )
                self._process = None
