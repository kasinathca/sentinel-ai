from __future__ import annotations

from datetime import datetime, timedelta, timezone
import os
from pathlib import Path
import subprocess
import sys
import unittest
from uuid import UUID

from app.ai_integration.criterion import RollingViolenceCriterionEngine, StreamKey


ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = ROOT / "backend"


def probe_threshold(value: str | None) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(BACKEND_ROOT)
    if value is None:
        environment.pop("SENTINEL_EXPERIMENTAL_THRESHOLD", None)
    else:
        environment["SENTINEL_EXPERIMENTAL_THRESHOLD"] = value
    return subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "from app.ai_integration.constants import "
                "EXPERIMENTAL_THRESHOLD_ACTIVE,LIVE_THRESHOLD;"
                "print(LIVE_THRESHOLD,EXPERIMENTAL_THRESHOLD_ACTIVE)"
            ),
        ],
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )


class ExperimentalThresholdConfigurationTests(unittest.TestCase):
    def test_unset_environment_preserves_qualified_threshold(self) -> None:
        result = probe_threshold(None)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "0.906 False")

    def test_explicit_080_enables_experimental_threshold(self) -> None:
        result = probe_threshold("0.80")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "0.8 True")

    def test_invalid_or_unsupported_values_fail_explicitly(self) -> None:
        for value in ("not-a-number", "nan", "inf", "-0.1", "1.1", "0.81"):
            with self.subTest(value=value):
                result = probe_threshold(value)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("SENTINEL_EXPERIMENTAL_THRESHOLD", result.stderr)

    def test_080_keeps_complete_history_three_of_five(self) -> None:
        engine = RollingViolenceCriterionEngine()
        key = StreamKey(
            camera_id=UUID("33333333-3333-4333-8333-333333333333"),
            model_version_id=UUID("6d22f83d-17f8-5ecf-9f0f-246fa326ec72"),
            source_session_id=UUID("22222222-2222-4222-8222-222222222222"),
        )
        started = datetime(2026, 10, 16, tzinfo=timezone.utc)
        states = []
        for index, score in enumerate((0.85, 0.79, 0.85, 0.79, 0.85)):
            states.append(
                engine.observe(
                    key=key,
                    score=score,
                    window_started_at=started + timedelta(seconds=index),
                    threshold=0.80,
                    n_required=3,
                    m_history=5,
                )
            )
        self.assertTrue(states[0].score_positive)
        self.assertFalse(states[1].score_positive)
        self.assertFalse(any(state.candidate_condition for state in states[:4]))
        self.assertTrue(states[4].complete_history)
        self.assertEqual(states[4].positive_count, 3)
        self.assertTrue(states[4].candidate_condition)


if __name__ == "__main__":
    unittest.main()
