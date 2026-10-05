from __future__ import annotations

import copy
import unittest
from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy import select, create_engine
from sqlalchemy.pool import StaticPool

from app.ai_integration.constants import MODEL_VERSION_ID
from app.ai_integration.database_model_registry import DatabaseModelRegistry
from app.ai_integration import router as ai_router
from app.ai_integration.service import ViolenceWorkerResultService
from app.cameras import router as camera_router
from app.db.base import Base
from app.db.models import Camera, Event, ViolenceEventContext
from app.db.seed import seed_frozen_violence_model
from app.db.session import build_engine, build_session_factory
from app.events.persistence import ViolenceEventPersistenceService
from app.events.violence_conditions import RecordingViolenceConditionConsumer, ViolenceConditionEvaluation
from app.events import router as event_router
from app.main import create_app


CAMERA_ID = UUID("33333333-3333-4333-8333-333333333333")
MODEL_ID = UUID(MODEL_VERSION_ID)
BASE_PAYLOAD = {
    "schema_version": "1",
    "job_id": "11111111-1111-4111-8111-111111111111",
    "correlation_id": "22222222-2222-4222-8222-222222222222",
    "camera_id": str(CAMERA_ID),
    "window": {"started_at": "2026-09-12T07:00:00Z", "ended_at": "2026-09-12T07:00:01Z"},
    "status": "success",
    "model": {"model_version_id": str(MODEL_ID), "task": "violence_fighting"},
    "result": {
        "label": "fighting",
        "score": 0.94,
        "score_semantics": "uncalibrated sigmoid score for the fighting positive class from EXP-VIO-TEMPORAL-001; higher means more fighting-like",
    },
}


class APIContractTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(
            "sqlite+pysqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(self.engine)
        self.sessions = build_session_factory(self.engine)
        seed_frozen_violence_model(self.sessions)
        with self.sessions.begin() as session:
            session.add(Camera(id=CAMERA_ID, name="North Entrance", description="Main gate", source_kind="file", enabled=True))

        def override_db():
            with self.sessions() as session:
                yield session

        self.app = create_app()
        for module in (camera_router, event_router, ai_router):
            self.app.dependency_overrides[module.get_db] = override_db
        self.consumer = RecordingViolenceConditionConsumer()
        self.old_service = ai_router._worker_service
        ai_router._worker_service = ViolenceWorkerResultService(
            condition_consumer=self.consumer,
            model_registry=DatabaseModelRegistry(self.sessions),
        )
        self.client = TestClient(self.app)

    def tearDown(self):
        ai_router._worker_service = self.old_service
        self.app.dependency_overrides.clear()
        self.engine.dispose()

    def _worker_result(self, index: int, score: float = 0.94):
        payload = copy.deepcopy(BASE_PAYLOAD)
        start = datetime(2026, 9, 12, 7, 0, tzinfo=timezone.utc) + timedelta(seconds=index)
        payload["window"]["started_at"] = start.isoformat().replace("+00:00", "Z")
        payload["window"]["ended_at"] = (start + timedelta(seconds=1)).isoformat().replace("+00:00", "Z")
        payload["job_id"] = f"11111111-1111-4111-8111-{index:012d}"
        payload["result"]["score"] = score
        return payload

    def test_health_route(self):
        response = self.client.get("/api/v1/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["service"], "sentinel-api")

    def test_camera_create_list_detail_update_and_health_contract(self):
        created = self.client.post("/api/v1/cameras", json={"name": "Dock", "description": "Loading bay", "source_kind": "file"})
        self.assertEqual(created.status_code, 201)
        body = created.json()["data"]
        self.assertEqual(body["description"], "Loading bay")
        self.assertEqual(body["health"], {"state": "unknown", "last_frame_at": None, "last_health_check_at": None})
        self.assertNotIn("source_locator", body)
        self.assertEqual(self.client.get("/api/v1/cameras").json()["data"][0]["health"]["state"], "unknown")
        camera_id = body["id"]
        self.assertEqual(self.client.get(f"/api/v1/cameras/{camera_id}").status_code, 200)
        changed = self.client.patch(f"/api/v1/cameras/{camera_id}", json={"name": "Dock North", "description": None})
        self.assertEqual(changed.json()["data"]["name"], "Dock North")
        self.assertIsNone(changed.json()["data"]["description"])
        health = self.client.get(f"/api/v1/cameras/{camera_id}/health").json()["data"]
        self.assertEqual(health["state"], "unknown")
        self.assertFalse(self.client.get("/api/v1/cameras?enabled=false").json()["data"])

    def test_camera_invalid_and_not_found(self):
        self.assertEqual(self.client.get("/api/v1/cameras/not-a-uuid").status_code, 422)
        self.assertEqual(self.client.get("/api/v1/cameras/aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa").status_code, 404)
        self.assertEqual(self.client.post("/api/v1/cameras", json={"name": "", "source_kind": "file"}).status_code, 422)
        self.assertEqual(self.client.post("/api/v1/cameras", json={"name": "x", "source_kind": "file", "unexpected": 1}).status_code, 422)

    def test_worker_invalid_unknown_model_and_unknown_camera(self):
        invalid = self.client.post("/api/v1/ai/violence/results", json={**BASE_PAYLOAD, "unexpected": True})
        self.assertEqual(invalid.status_code, 422)
        unknown_model = copy.deepcopy(BASE_PAYLOAD)
        unknown_model["model"]["model_version_id"] = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
        self.assertEqual(self.client.post("/api/v1/ai/violence/results", json=unknown_model).status_code, 422)
        unknown_camera = copy.deepcopy(BASE_PAYLOAD)
        unknown_camera["camera_id"] = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
        self.assertEqual(self.client.post("/api/v1/ai/violence/results", json=unknown_camera).status_code, 404)

    def test_worker_out_of_order_is_conflict_without_event(self):
        self.assertEqual(self.client.post("/api/v1/ai/violence/results", json=self._worker_result(3)).status_code, 200)
        out_of_order = self.client.post("/api/v1/ai/violence/results", json=self._worker_result(2))
        self.assertEqual(out_of_order.status_code, 409)
        with self.sessions() as session:
            self.assertEqual(len(list(session.scalars(select(Event)))), 0)

    def test_normal_worker_result_and_failure_do_not_create_events(self):
        normal = self.client.post("/api/v1/ai/violence/results", json=self._worker_result(0, 0.01))
        self.assertEqual(normal.status_code, 200)
        self.assertFalse(normal.json()["data"]["candidate_condition"])
        failed = copy.deepcopy(BASE_PAYLOAD)
        failed["status"] = "failed"
        failed.pop("window")
        failed.pop("model")
        failed.pop("result")
        failed["error"] = {"code": "INFERENCE_FAILED", "message": "Inference failed."}
        failed_response = self.client.post("/api/v1/ai/violence/results", json=failed)
        self.assertEqual(failed_response.status_code, 422)
        self.assertEqual(failed_response.json()["detail"], {"code": "INFERENCE_FAILED", "message": "Inference failed."})
        with self.sessions() as session:
            self.assertEqual(len(list(session.scalars(select(Event)))), 0)

    def test_candidate_then_repeated_positive_windows_do_not_flood_events(self):
        responses = [self.client.post("/api/v1/ai/violence/results", json=self._worker_result(i)) for i in range(7)]
        self.assertTrue(all(response.status_code == 200 for response in responses))
        self.assertTrue(responses[4].json()["data"]["candidate_condition"])
        self.assertEqual(responses[4].json()["data"]["event_lifecycle"], "awaiting_domain_policy")
        self.assertFalse(responses[4].json()["data"]["event_persisted"])
        self.assertTrue(responses[6].json()["data"]["candidate_condition"])
        with self.sessions() as session:
            self.assertEqual(len(list(session.scalars(select(Event)))), 0)
        self.assertEqual(len(self.consumer.evaluations), 7)

    def test_event_public_dto_and_ordering(self):
        start = datetime(2026, 9, 12, 7, 0, tzinfo=timezone.utc)
        evaluation = ViolenceConditionEvaluation(
            camera_id=CAMERA_ID, model_version_id=MODEL_ID,
            job_id=UUID(BASE_PAYLOAD["job_id"]), correlation_id=UUID(BASE_PAYLOAD["correlation_id"]),
            window_started_at=start, window_ended_at=start + timedelta(seconds=1), score=0.94,
            score_positive=True, history_count=5, positive_count=3, complete_history=True,
            candidate_condition=True, threshold_snapshot=0.906, n_required_snapshot=3,
            m_history_snapshot=5, score_semantics=BASE_PAYLOAD["result"]["score_semantics"],
        )
        first = ViolenceEventPersistenceService(self.sessions).create_from_qualified_condition(evaluation=evaluation, requires_attention=True)
        later = ViolenceConditionEvaluation(**{**evaluation.__dict__, "window_ended_at": start + timedelta(seconds=5), "window_started_at": start + timedelta(seconds=4)})
        ViolenceEventPersistenceService(self.sessions).create_from_qualified_condition(evaluation=later, requires_attention=True)
        listed = self.client.get("/api/v1/events").json()["data"]
        self.assertTrue(listed[0]["occurred_at"].startswith("2026-09-12T07:00:05"))
        detail = self.client.get(f"/api/v1/events/{first.event_id}")
        self.assertEqual(detail.status_code, 200)
        event = detail.json()["data"]
        self.assertEqual(event["event_type"], "violence_fighting")
        self.assertEqual(event["camera"], {"id": str(CAMERA_ID), "name": "North Entrance"})
        self.assertIn("severity", event)
        self.assertIn("status", event)
        self.assertEqual(event["acknowledgement"], {"acknowledged": False, "acknowledged_by": [], "first_acknowledged_at": None})
        self.assertEqual(event["evidence"], {"available_count": 0, "pending_count": 0, "failed_count": 0})
        self.assertEqual(event["context"]["score"], 0.94)
        self.assertEqual(event["context"]["event_threshold"], 0.906)
        self.assertNotIn("event_type_code", event)
        self.assertNotIn("severity_code", event)
        self.assertNotIn("violence_context", event)
        self.assertEqual(self.client.get("/api/v1/events/not-a-uuid").status_code, 422)
        self.assertEqual(self.client.get("/api/v1/events/aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa").status_code, 404)
