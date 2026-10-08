from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
import threading
import time
import unittest
from uuid import UUID, uuid4

from app.ai_integration.constants import MODEL_VERSION_ID, SCORE_SEMANTICS
from app.ai_integration.service import ViolenceProcessingOutcome
from app.demo.ai_orchestrator import DemoAIOrchestrator
from app.demo.clip_catalog import DemoClip
from app.events.violence_conditions import ViolenceConditionEvaluation


class RecordingOrchestrator(DemoAIOrchestrator):
    def __init__(self) -> None:
        super().__init__(lambda payload: payload)
        self.pass_starts: list[datetime] = []
        self.active_passes = 0
        self.max_active_passes = 0
        self.first_pass_started = threading.Event()
        self.release_first_pass = threading.Event()

    def _run_pass(self, clip, source_session_id, generation, started_at):
        del clip, source_session_id
        with self._lock:
            self.active_passes += 1
            self.max_active_passes = max(self.max_active_passes, self.active_passes)
            self.pass_starts.append(started_at)
            self._latest_window_ended_at = started_at + timedelta(seconds=2)
        if len(self.pass_starts) == 1:
            self.first_pass_started.set()
            self.release_first_pass.wait(timeout=2)
        with self._lock:
            self.active_passes -= 1
        return generation == self._generation


class DemoAIOrchestratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.clip = DemoClip("clip", "Clip", "clip.mp4", Path("clip.mp4"))
        self.session_id = uuid4()

    def test_real_loop_boundaries_queue_sequential_monotonic_passes(self) -> None:
        orchestrator = RecordingOrchestrator()
        orchestrator.start(self.clip, self.session_id)
        self.assertTrue(orchestrator.first_pass_started.wait(timeout=1))
        boundary = datetime.now(timezone.utc)
        orchestrator.loop_restarted(self.clip, self.session_id, boundary)
        orchestrator.loop_restarted(self.clip, self.session_id, boundary)
        orchestrator.release_first_pass.set()
        deadline = time.monotonic() + 2
        while orchestrator.status().analyzed_passes < 3 and time.monotonic() < deadline:
            time.sleep(0.01)
        self.assertEqual(orchestrator.status().analyzed_passes, 3)
        self.assertEqual(orchestrator.max_active_passes, 1)
        self.assertEqual(len(orchestrator.pass_starts), 3)
        self.assertLess(orchestrator.pass_starts[0], orchestrator.pass_starts[1])
        self.assertLess(orchestrator.pass_starts[1], orchestrator.pass_starts[2])
        self.assertEqual(orchestrator.status().state, "waiting-for-next-loop")
        orchestrator.stop()

    def test_status_exposes_threshold_and_temporal_diagnostics(self) -> None:
        orchestrator = DemoAIOrchestrator(lambda payload: payload)
        started = datetime.now(timezone.utc)
        evaluation = ViolenceConditionEvaluation(
            camera_id=uuid4(),
            model_version_id=UUID(MODEL_VERSION_ID),
            job_id=uuid4(),
            correlation_id=self.session_id,
            window_started_at=started,
            window_ended_at=started + timedelta(seconds=1),
            score=0.95,
            score_positive=True,
            history_count=3,
            positive_count=1,
            complete_history=False,
            candidate_condition=False,
            threshold_snapshot=0.906,
            n_required_snapshot=3,
            m_history_snapshot=5,
            score_semantics=SCORE_SEMANTICS,
        )
        with orchestrator._lock:
            orchestrator._generation = 7
            orchestrator._status = orchestrator._status.__class__(
                state="processing", source_session_id=self.session_id
            )
        orchestrator._accept_outcome(
            7, self.session_id, ViolenceProcessingOutcome(evaluation, None)
        )
        public = orchestrator.status().to_public_dict()
        self.assertTrue(public["latest_score_positive"])
        self.assertEqual(public["history_count"], 3)
        self.assertEqual(public["positive_count"], 1)
        self.assertFalse(public["complete_history"])
        self.assertFalse(public["candidate_condition"])
        self.assertEqual(public["processed_windows_total"], 1)
        self.assertEqual(public["n_required"], 3)
        self.assertEqual(public["m_history"], 5)


if __name__ == "__main__":
    unittest.main()
