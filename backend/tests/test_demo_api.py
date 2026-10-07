from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from fastapi.testclient import TestClient

from app.demo.clip_catalog import DemoClipCatalog
from app.demo.controller import PlaybackCallbacks, VirtualCameraController
from app.main import create_app


class FakeReplayAdapter:
    def __init__(self) -> None:
        self.callbacks: PlaybackCallbacks | None = None
        self.start_count = 0
        self.stop_count = 0
        self.restart_count = 0

    def start(self, clip, callbacks: PlaybackCallbacks) -> None:
        self.start_count += 1
        self.callbacks = callbacks
        callbacks.first_frame()

    def stop(self) -> None:
        self.stop_count += 1

    def restart(self, callbacks: PlaybackCallbacks) -> None:
        self.restart_count += 1
        self.callbacks = callbacks
        callbacks.first_frame()


class DemoAPITests(unittest.TestCase):
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
        self.adapter = FakeReplayAdapter()
        self.controller = VirtualCameraController(
            lambda: DemoClipCatalog(self.root), self.adapter
        )
        self.client = TestClient(create_app(demo_controller=self.controller))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_catalog_response_uses_public_fields_only(self) -> None:
        response = self.client.get("/api/v1/demo/clips")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(
            body["data"],
            [
                {"clip_id": "scenario-01", "display_name": "Scenario 01"},
                {"clip_id": "scenario-02", "display_name": "Scenario 02"},
            ],
        )
        self.assertNotIn(str(self.root), response.text)

    def test_selection_start_status_stop_and_restart(self) -> None:
        selected = self.client.put(
            "/api/v1/demo/source", json={"clip_id": "scenario-01"}
        )
        self.assertEqual(selected.status_code, 200)
        self.assertEqual(selected.json()["data"]["state"], "ready")

        started = self.client.post("/api/v1/demo/source/start")
        self.assertEqual(started.status_code, 200)
        self.assertEqual(started.json()["data"]["state"], "playing")
        self.assertEqual(self.adapter.start_count, 1)

        status = self.client.get("/api/v1/demo/source/status")
        self.assertEqual(status.status_code, 200)
        self.assertEqual(status.json()["data"]["clip_id"], "scenario-01")
        self.assertNotIn(str(self.root), status.text)

        restarted = self.client.post("/api/v1/demo/source/restart")
        self.assertEqual(restarted.status_code, 200)
        self.assertEqual(restarted.json()["data"]["state"], "playing")
        self.assertEqual(self.adapter.restart_count, 1)

        stopped = self.client.post("/api/v1/demo/source/stop")
        self.assertEqual(stopped.status_code, 200)
        self.assertEqual(stopped.json()["data"]["state"], "stopped")
        self.assertEqual(self.adapter.stop_count, 1)

    def test_unknown_clip_and_path_body_fail_safely(self) -> None:
        unknown = self.client.put(
            "/api/v1/demo/source", json={"clip_id": "not-registered"}
        )
        self.assertEqual(unknown.status_code, 404)
        self.assertEqual(unknown.json()["error"]["code"], "DEMO_CLIP_NOT_FOUND")
        self.assertNotIn(str(self.root), unknown.text)

        path_input = self.client.put(
            "/api/v1/demo/source",
            json={"clip_id": "scenario-01", "path": "C:\\private\\clip.mp4"},
        )
        self.assertEqual(path_input.status_code, 422)
        self.assertEqual(path_input.json()["error"]["code"], "VALIDATION_ERROR")

        empty_id = self.client.put("/api/v1/demo/source", json={"clip_id": "   "})
        self.assertEqual(empty_id.status_code, 422)
        self.assertEqual(empty_id.json()["error"]["code"], "VALIDATION_ERROR")

    def test_invalid_state_and_unavailable_adapter_errors(self) -> None:
        before_selection = self.client.post("/api/v1/demo/source/start")
        self.assertEqual(before_selection.status_code, 409)
        self.assertEqual(
            before_selection.json()["error"]["code"], "DEMO_SOURCE_STATE_CONFLICT"
        )

        unavailable_controller = VirtualCameraController(
            lambda: DemoClipCatalog(self.root), replay_adapter=None
        )
        unavailable_client = TestClient(
            create_app(demo_controller=unavailable_controller)
        )
        unavailable_client.put(
            "/api/v1/demo/source", json={"clip_id": "scenario-01"}
        )
        unavailable = unavailable_client.post("/api/v1/demo/source/start")
        self.assertEqual(unavailable.status_code, 503)
        self.assertEqual(unavailable.json()["error"]["code"], "SOURCE_UNAVAILABLE")
        self.assertNotIn(str(self.root), unavailable.text)

    def test_source_change_while_playing_is_conflict(self) -> None:
        self.client.put("/api/v1/demo/source", json={"clip_id": "scenario-01"})
        self.client.post("/api/v1/demo/source/start")
        response = self.client.put(
            "/api/v1/demo/source", json={"clip_id": "scenario-02"}
        )
        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response.json()["error"]["code"], "DEMO_SOURCE_STATE_CONFLICT"
        )

    def test_demo_control_route_is_local_only(self) -> None:
        remote = TestClient(
            create_app(demo_controller=self.controller), client=("192.0.2.10", 12345)
        )
        response = remote.get("/api/v1/demo/source/status")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["error"]["code"], "FORBIDDEN")


if __name__ == "__main__":
    unittest.main()
