"""Continuous bridge from the looping demo source to the frozen AI worker."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone
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
    latest_score_positive: bool = False
    history_count: int = 0
    positive_count: int = 0
    complete_history: bool = False
    candidate_condition: bool = False
    event_id: UUID | None = None
    processed_windows_total: int = 0
    analyzed_passes: int = 0
    error: str | None = None

    def to_public_dict(self) -> dict[str, object]:
        return {
            "state": self.state,
            "source_session_id": (
                str(self.source_session_id) if self.source_session_id else None
            ),
            "latest_score": self.latest_score,
            "latest_score_positive": self.latest_score_positive,
            "history_count": self.history_count,
            "positive_count": self.positive_count,
            "complete_history": self.complete_history,
            "candidate_condition": self.candidate_condition,
            "event_id": str(self.event_id) if self.event_id else None,
            "processed_windows": self.processed_windows_total,
            "processed_windows_total": self.processed_windows_total,
            "analyzed_passes": self.analyzed_passes,
            "error": self.error,
            "model_version_id": MODEL_VERSION_ID,
            "threshold": LIVE_THRESHOLD,
            "n_required": LIVE_N_REQUIRED,
            "m_history": LIVE_M_HISTORY,
            "criterion": f"{LIVE_N_REQUIRED}-of-{LIVE_M_HISTORY}",
            "score_semantics": SCORE_SEMANTICS,
        }


class DemoAIOrchestrator:
    """Analyze every real replay pass sequentially for one source session."""

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
        self._condition = threading.Condition(self._lock)
        self._stop_event = threading.Event()
        self._worker: threading.Thread | None = None
        self._process: subprocess.Popen[str] | None = None
        self._generation = 0
        self._pending_passes: deque[datetime] = deque()
        self._latest_window_ended_at: datetime | None = None
        self._status = DemoAIStatus()

    def start(self, clip: DemoClip, source_session_id: UUID) -> None:
        self._stop_worker(reset_status=True)
        self._begin(clip, source_session_id, datetime.now(timezone.utc))

    def restart(self, clip: DemoClip, source_session_id: UUID) -> None:
        """Restart playback without resetting same-session criterion state."""
        with self._lock:
            previous = self._status
        self._stop_worker(reset_status=False)
        with self._lock:
            self._status = (
                replace(previous, state="starting", error=None)
                if previous.source_session_id == source_session_id
                else DemoAIStatus(state="starting", source_session_id=source_session_id)
            )
        self._begin(clip, source_session_id, datetime.now(timezone.utc), reset=False)

    def loop_restarted(
        self,
        clip: DemoClip,
        source_session_id: UUID,
        started_at: datetime | None = None,
    ) -> None:
        """Queue one fresh inference pass at an actual FFmpeg loop boundary."""
        del clip
        with self._condition:
            if (
                self._worker is None
                or self._stop_event.is_set()
                or self._status.source_session_id != source_session_id
                or self._status.state == "failed"
            ):
                return
            self._pending_passes.append(started_at or datetime.now(timezone.utc))
            self._condition.notify_all()

    def stop(self) -> None:
        self._stop_worker(reset_status=True)

    def status(self) -> DemoAIStatus:
        with self._lock:
            return self._status

    def _begin(
        self,
        clip: DemoClip,
        source_session_id: UUID,
        started_at: datetime,
        *,
        reset: bool = True,
    ) -> None:
        with self._condition:
            self._generation += 1
            generation = self._generation
            self._stop_event.clear()
            self._pending_passes.clear()
            self._pending_passes.append(started_at)
            if reset:
                self._latest_window_ended_at = None
                self._status = DemoAIStatus(state="starting", source_session_id=source_session_id)
            self._worker = threading.Thread(
                target=self._run_manager,
                args=(clip, source_session_id, generation),
                name="sentinel-demo-ai",
                daemon=True,
            )
            self._worker.start()

    def _stop_worker(self, *, reset_status: bool) -> None:
        self._stop_event.set()
        with self._condition:
            process = self._process
            worker = self._worker
            self._generation += 1
            self._pending_passes.clear()
            self._condition.notify_all()
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
            if reset_status:
                self._status = DemoAIStatus(state="stopped")

    def _run_manager(
        self, clip: DemoClip, source_session_id: UUID, generation: int
    ) -> None:
        while not self._stop_event.is_set():
            with self._condition:
                while not self._pending_passes and not self._stop_event.is_set():
                    if generation == self._generation:
                        self._status = replace(self._status, state="waiting-for-next-loop")
                    self._condition.wait(timeout=0.5)
                if self._stop_event.is_set() or generation != self._generation:
                    return
                started_at = self._pending_passes.popleft()
                if (
                    self._latest_window_ended_at is not None
                    and started_at <= self._latest_window_ended_at
                ):
                    started_at = self._latest_window_ended_at + timedelta(
                        microseconds=1
                    )
            if not self._run_pass(clip, source_session_id, generation, started_at):
                return
            with self._lock:
                if generation == self._generation:
                    self._status = replace(
                        self._status,
                        state="waiting-for-next-loop",
                        analyzed_passes=self._status.analyzed_passes + 1,
                    )

    def _run_pass(
        self,
        clip: DemoClip,
        source_session_id: UUID,
        generation: int,
        started_at: datetime,
    ) -> bool:
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
                return False
            with self._lock:
                if generation != self._generation:
                    process.terminate()
                    return False
                self._process = process
                self._status = replace(self._status, state="processing", error=None)

            assert process.stdout is not None
            try:
                for line in process.stdout:
                    if self._stop_event.is_set() or generation != self._generation:
                        process.terminate()
                        return False
                    payload = json.loads(line)
                    if payload.get("status") == "failed":
                        self._fail(
                            generation,
                            payload.get("error", {}).get(
                                "message", "AI inference failed."
                            ),
                        )
                        return False
                    ended_at = datetime.fromisoformat(
                        payload["window"]["ended_at"].replace("Z", "+00:00")
                    )
                    delay = (ended_at - datetime.now(timezone.utc)).total_seconds()
                    if delay > 0 and self._stop_event.wait(delay):
                        process.terminate()
                        return False
                    outcome = self._result_consumer(payload)
                    self._accept_outcome(generation, source_session_id, outcome)
            except Exception:
                self._fail(generation, "AI inference result processing failed.")
                process.terminate()
                return False
            return_code = process.wait()
            with self._lock:
                if self._process is process:
                    self._process = None
            if return_code != 0:
                if not self._stop_event.is_set():
                    self._fail(generation, "The AI worker exited before completing inference.")
                return False
            return True

    def _accept_outcome(
        self,
        generation: int,
        source_session_id: UUID,
        outcome: ViolenceProcessingOutcome,
    ) -> None:
        with self._lock:
            if generation != self._generation:
                return
            evaluation = outcome.evaluation
            self._latest_window_ended_at = evaluation.window_ended_at
            self._status = replace(
                self._status,
                state="processing",
                source_session_id=source_session_id,
                latest_score=evaluation.score,
                latest_score_positive=evaluation.score_positive,
                history_count=evaluation.history_count,
                positive_count=evaluation.positive_count,
                complete_history=evaluation.complete_history,
                candidate_condition=evaluation.candidate_condition,
                event_id=outcome.event_id or self._status.event_id,
                processed_windows_total=self._status.processed_windows_total + 1,
                error=None,
            )

    def _fail(self, generation: int, message: str) -> None:
        with self._lock:
            if generation == self._generation:
                self._status = replace(self._status, state="failed", error=message)
                self._process = None
