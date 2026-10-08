from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from app.demo.clip_catalog import DemoClipCatalog, DemoClipNotFound
from app.demo.controller import (
    DemoControllerError,
    DemoSourceState,
    PlaybackCallbacks,
    VirtualCameraController,
)


class FakeReplayAdapter:
    def __init__(self, *, emit_first_frame: bool = False) -> None:
        self.emit_first_frame = emit_first_frame
        self.callbacks: PlaybackCallbacks | None = None
        self.started: list[str] = []
        self.stop_count = 0
        self.restart_count = 0

    def start(self, clip, callbacks: PlaybackCallbacks) -> None:
        self.started.append(clip.clip_id)
        self.callbacks = callbacks
        if self.emit_first_frame:
            callbacks.first_frame()

    def stop(self) -> None:
        self.stop_count += 1

    def restart(self, callbacks: PlaybackCallbacks) -> None:
        self.restart_count += 1
        self.callbacks = callbacks
        if self.emit_first_frame:
            callbacks.first_frame()


class FakeAIOrchestrator:
    def __init__(self) -> None:
        self.starts = []
        self.restarts = []
        self.loop_restarts = []
        self.stop_count = 0

    def start(self, clip, source_session_id) -> None:
        self.starts.append((clip.clip_id, source_session_id))

    def restart(self, clip, source_session_id) -> None:
        self.restarts.append((clip.clip_id, source_session_id))

    def loop_restarted(self, clip, source_session_id, started_at=None) -> None:
        self.loop_restarts.append((clip.clip_id, source_session_id, started_at))

    def stop(self) -> None:
        self.stop_count += 1


class VirtualCameraControllerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "clips").mkdir()
        (self.root / "clips" / "scenario.mp4").write_bytes(b"test media")
        (self.root / "clips" / "scenario_02.mp4").write_bytes(b"test media 2")
        (self.root / "manifest.json").write_text(
            json.dumps(
                {
                    "schema_version": "1",
                    "clips": [
                        {
                            "clip_id": "scenario-01",
                            "display_name": "Scenario 01",
                            "relative_path": "clips/scenario.mp4",
                        },
                        {
                            "clip_id": "scenario-02",
                            "display_name": "Scenario 02",
                            "relative_path": "clips/scenario_02.mp4",
                        },
                    ],
                }
            ),
            encoding="utf-8",
        )
        self.catalog = DemoClipCatalog(self.root)
        self.adapter = FakeReplayAdapter()
        self.controller = VirtualCameraController(lambda: self.catalog, self.adapter)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_initial_state_and_selection(self) -> None:
        initial = self.controller.snapshot()
        self.assertEqual(initial.state, DemoSourceState.IDLE)
        self.assertIsNone(initial.clip_id)
        self.assertIsNone(initial.session_id)

        selected = self.controller.select_source("scenario-01")
        self.assertEqual(selected.state, DemoSourceState.READY)
        self.assertEqual(selected.clip_id, "scenario-01")
        self.assertNotIn(str(self.root), str(selected.to_public_dict()))

    def test_unknown_clip_is_rejected(self) -> None:
        with self.assertRaises(DemoClipNotFound):
            self.controller.select_source("unknown")

    def test_start_requires_selection_and_duplicate_start_is_rejected(self) -> None:
        with self.assertRaises(DemoControllerError) as missing_selection:
            self.controller.start()
        self.assertEqual(missing_selection.exception.http_status, 409)

        self.controller.select_source("scenario-01")
        self.controller.start()
        self.assertEqual(self.controller.snapshot().state, DemoSourceState.STARTING)
        with self.assertRaises(DemoControllerError) as duplicate:
            self.controller.start()
        self.assertEqual(duplicate.exception.http_status, 409)
        self.assertEqual(self.adapter.started, ["scenario-01"])

    def test_source_cannot_be_changed_while_active(self) -> None:
        self.controller.select_source("scenario-01")
        self.controller.start()
        with self.assertRaises(DemoControllerError) as conflict:
            self.controller.select_source("scenario-02")
        self.assertEqual(conflict.exception.http_status, 409)
        self.assertEqual(self.adapter.started, ["scenario-01"])

    def test_first_frame_loop_and_stop_transitions(self) -> None:
        self.controller.select_source("scenario-01")
        self.controller.start()
        first_session = self.controller.snapshot().session_id
        self.assertIsNotNone(first_session)
        callbacks = self.adapter.callbacks
        self.assertIsNotNone(callbacks)

        callbacks.first_frame(125)
        self.assertEqual(self.controller.snapshot().state, DemoSourceState.PLAYING)
        callbacks.position_changed(900)
        self.assertEqual(self.controller.snapshot().position_ms, 900)

        callbacks.loop_restart_started()
        self.assertEqual(self.controller.snapshot().state, DemoSourceState.LOOP_RESTARTING)
        callbacks.loop_restart_completed()
        looping = self.controller.snapshot()
        self.assertEqual(looping.state, DemoSourceState.PLAYING)
        self.assertEqual(looping.loop_count, 1)
        self.assertEqual(looping.session_id, first_session)

        stale_callbacks = callbacks
        stopped = self.controller.stop()
        self.assertEqual(stopped.state, DemoSourceState.STOPPED)
        self.assertIsNone(stopped.session_id)
        self.assertEqual(self.adapter.stop_count, 1)
        self.controller.stop()
        self.assertEqual(self.adapter.stop_count, 1)
        stale_callbacks.first_frame()
        self.assertEqual(self.controller.snapshot().state, DemoSourceState.STOPPED)

        self.controller.start()
        next_session = self.controller.snapshot().session_id
        self.assertIsNotNone(next_session)
        self.assertNotEqual(next_session, first_session)

    def test_restart_requires_an_active_selected_source(self) -> None:
        with self.assertRaises(DemoControllerError) as no_selection:
            self.controller.restart()
        self.assertEqual(no_selection.exception.http_status, 409)
        self.controller.select_source("scenario-01")
        with self.assertRaises(DemoControllerError) as stopped:
            self.controller.restart()
        self.assertEqual(stopped.exception.http_status, 409)

    def test_source_failure_is_explicit_and_safe(self) -> None:
        self.controller.select_source("scenario-01")
        self.controller.start()
        self.adapter.callbacks.failed()
        snapshot = self.controller.snapshot()
        self.assertEqual(snapshot.state, DemoSourceState.FAILED)
        self.assertNotIn("scenario.mp4", str(snapshot.to_public_dict()))

    def test_start_after_selected_media_disappears_fails_safely(self) -> None:
        self.controller.select_source("scenario-01")
        (self.root / "clips" / "scenario.mp4").unlink()
        with self.assertRaises(DemoControllerError) as failure:
            self.controller.start()
        self.assertEqual(failure.exception.code, "SOURCE_UNAVAILABLE")
        self.assertEqual(self.controller.snapshot().state, DemoSourceState.FAILED)

    def test_missing_replay_adapter_does_not_claim_playing(self) -> None:
        controller = VirtualCameraController(lambda: self.catalog, replay_adapter=None)
        controller.select_source("scenario-01")
        with self.assertRaises(DemoControllerError) as failure:
            controller.start()
        self.assertEqual(failure.exception.http_status, 503)
        self.assertEqual(controller.snapshot().state, DemoSourceState.FAILED)

    def test_ai_orchestration_uses_and_cleans_up_the_source_session(self) -> None:
        ai = FakeAIOrchestrator()
        controller = VirtualCameraController(
            lambda: self.catalog, self.adapter, ai_orchestrator=ai
        )
        controller.select_source("scenario-01")
        started = controller.start()
        self.assertEqual(ai.starts, [("scenario-01", started.session_id)])
        self.adapter.callbacks.first_frame()
        self.adapter.callbacks.loop_restart_started()
        self.adapter.callbacks.loop_restart_completed()
        self.assertEqual(len(ai.loop_restarts), 1)
        self.assertEqual(ai.loop_restarts[0][:2], ("scenario-01", started.session_id))
        restarted = controller.restart()
        self.assertEqual(restarted.session_id, started.session_id)
        self.assertEqual(ai.restarts, [("scenario-01", started.session_id)])
        controller.stop()
        self.assertEqual(ai.stop_count, 1)


if __name__ == "__main__":
    unittest.main()
