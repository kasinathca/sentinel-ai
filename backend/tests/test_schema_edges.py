from __future__ import annotations

import copy
import unittest

from app.ai_integration.errors import WorkerContractValidationError
from app.ai_integration.service import ViolenceWorkerResultService
from app.events.violence_conditions import RecordingViolenceConditionConsumer

BASE = {
    "schema_version": "1",
    "job_id": "11111111-1111-4111-8111-111111111111",
    "correlation_id": "22222222-2222-4222-8222-222222222222",
    "camera_id": "33333333-3333-4333-8333-333333333333",
    "window": {
        "started_at": "2026-09-12T07:00:00.000Z",
        "ended_at": "2026-09-12T07:00:02.667Z",
    },
    "status": "success",
    "model": {
        "model_version_id": "6d22f83d-17f8-5ecf-9f0f-246fa326ec72",
        "task": "violence_fighting",
    },
    "result": {
        "label": "fighting",
        "score": 0.94,
        "score_semantics": "uncalibrated sigmoid score for the fighting positive class from EXP-VIO-TEMPORAL-001; higher means more fighting-like",
    },
}


class SchemaEdgeTests(unittest.TestCase):
    def service(self):
        return ViolenceWorkerResultService(
            condition_consumer=RecordingViolenceConditionConsumer()
        )

    def test_uuid_and_rfc3339_strings_are_accepted(self):
        result = self.service().consume_payload(copy.deepcopy(BASE))
        self.assertEqual(str(result.camera_id), BASE["camera_id"])

    def test_numeric_string_score_is_rejected(self):
        payload = copy.deepcopy(BASE)
        payload["result"]["score"] = "0.94"
        with self.assertRaises(WorkerContractValidationError):
            self.service().consume_payload(payload)

    def test_naive_timestamp_is_rejected(self):
        payload = copy.deepcopy(BASE)
        payload["window"]["started_at"] = "2026-09-12T07:00:00"
        with self.assertRaises(WorkerContractValidationError):
            self.service().consume_payload(payload)

    def test_wrong_model_id_is_rejected(self):
        payload = copy.deepcopy(BASE)
        payload["model"]["model_version_id"] = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
        from app.ai_integration.errors import UnknownModelError
        with self.assertRaises(UnknownModelError):
            self.service().consume_payload(payload)
