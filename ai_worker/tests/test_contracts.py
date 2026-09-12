from __future__ import annotations

import unittest

from sentinel_violence_runtime.contracts import (
    WorkerProcessingRequest,
    ViolenceWindowResult,
)
from sentinel_violence_runtime.errors import InvalidRequestError


class ContractTests(unittest.TestCase):
    def valid_request(self):
        return {
            "schema_version": "1",
            "job_id": "11111111-1111-4111-8111-111111111111",
            "correlation_id": "22222222-2222-4222-8222-222222222222",
            "source": {
                "camera_id": "33333333-3333-4333-8333-333333333333",
                "source_kind": "file",
                "source_locator_ref": "demo:fighting",
            },
            "tasks": ["violence_fighting"],
            "requested_at": "2026-09-12T07:00:00.000Z",
            "options": {},
        }

    def test_request_parses(self):
        req = WorkerProcessingRequest.from_dict(self.valid_request())
        self.assertEqual(req.schema_version, "1")
        self.assertEqual(req.source.source_locator_ref, "demo:fighting")

    def test_request_rejects_arbitrary_extra_task(self):
        data = self.valid_request()
        data["tasks"] = ["violence_fighting", "person_tracking"]
        with self.assertRaises(InvalidRequestError):
            WorkerProcessingRequest.from_dict(data)

    def test_request_rejects_non_uuid_camera(self):
        data = self.valid_request()
        data["source"]["camera_id"] = "camera-1"
        with self.assertRaises(InvalidRequestError):
            WorkerProcessingRequest.from_dict(data)

    def test_result_shape_matches_api_contract(self):
        result = ViolenceWindowResult(
            schema_version="1",
            job_id="11111111-1111-4111-8111-111111111111",
            correlation_id="22222222-2222-4222-8222-222222222222",
            camera_id="33333333-3333-4333-8333-333333333333",
            window_started_at="2026-09-12T07:00:00.000Z",
            window_ended_at="2026-09-12T07:00:02.667Z",
            model_version_id="6d22f83d-17f8-5ecf-9f0f-246fa326ec72",
            label="fighting",
            score=0.91,
            score_semantics="test semantics",
        ).to_dict()

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["model"]["task"], "violence_fighting")
        self.assertEqual(result["result"]["score"], 0.91)
        self.assertIn("window", result)
        self.assertNotIn("event_id", result)
        self.assertEqual(
            set(result.keys()),
            {
                "schema_version",
                "job_id",
                "correlation_id",
                "camera_id",
                "window",
                "status",
                "model",
                "result",
            },
        )


if __name__ == "__main__":
    unittest.main()
