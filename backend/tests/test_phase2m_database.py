from __future__ import annotations
from datetime import datetime,timedelta,timezone
import unittest
from uuid import UUID
from sqlalchemy import select
from app.ai_integration.constants import LIVE_M_HISTORY,LIVE_N_REQUIRED,LIVE_THRESHOLD,MODEL_VERSION_ID,SCORE_SEMANTICS
from app.ai_integration.database_model_registry import DatabaseModelRegistry
from app.db.base import Base
from app.db.models import AIModelVersion,Camera,Event,ViolenceEventContext,ViolenceEventPolicy
from app.db.seed import seed_frozen_violence_model
from app.db.session import build_engine,build_session_factory
from app.events.persistence import ViolenceEventPersistenceError,ViolenceEventPersistenceService
from app.events.violence_conditions import ViolenceConditionEvaluation
CAMERA_ID=UUID("33333333-3333-4333-8333-333333333333"); MODEL_ID=UUID(MODEL_VERSION_ID); JOB_ID=UUID("11111111-1111-4111-8111-111111111111"); CORRELATION_ID=UUID("22222222-2222-4222-8222-222222222222")
class Phase2MDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.engine=build_engine("sqlite+pysqlite:///:memory:"); Base.metadata.create_all(self.engine); self.sessions=build_session_factory(self.engine); seed_frozen_violence_model(self.sessions)
        with self.sessions.begin() as session: session.add(Camera(id=CAMERA_ID,name="Phase 2M Test Camera",source_kind="file",enabled=True))
    def tearDown(self): self.engine.dispose()
    def evaluation(self,candidate=True):
        start=datetime(2026,9,12,7,0,10,tzinfo=timezone.utc); end=start+timedelta(seconds=2.667)
        return ViolenceConditionEvaluation(camera_id=CAMERA_ID,model_version_id=MODEL_ID,job_id=JOB_ID,correlation_id=CORRELATION_ID,window_started_at=start,window_ended_at=end,score=0.9957476258277893,score_positive=True,history_count=5,positive_count=3,complete_history=True,candidate_condition=candidate,threshold_snapshot=LIVE_THRESHOLD,n_required_snapshot=LIVE_N_REQUIRED,m_history_snapshot=LIVE_M_HISTORY,score_semantics=SCORE_SEMANTICS)
    def test_seed_idempotent_and_frozen(self):
        seed_frozen_violence_model(self.sessions)
        with self.sessions() as session: versions=list(session.scalars(select(AIModelVersion))); policies=list(session.scalars(select(ViolenceEventPolicy)))
        self.assertEqual(len(versions),1); self.assertEqual(len(policies),1); self.assertEqual(policies[0].event_threshold_value,0.906); self.assertEqual(policies[0].n_required,3); self.assertEqual(policies[0].history_window_size,5); self.assertIsNone(policies[0].cooldown_ms)
    def test_database_registry_reconstructs_frozen_contract(self):
        selected=DatabaseModelRegistry(self.sessions).get_violence_model_version(MODEL_ID)
        self.assertEqual(selected.id,MODEL_ID); self.assertEqual(selected.event_threshold_value,0.906); self.assertEqual(selected.n_required,3); self.assertEqual(selected.history_window_size,5)
    def test_explicit_persistence_writes_event_and_context(self):
        persisted=ViolenceEventPersistenceService(self.sessions).create_from_qualified_condition(evaluation=self.evaluation(True),requires_attention=True)
        with self.sessions() as session: event=session.get(Event,persisted.event_id); context=session.get(ViolenceEventContext,persisted.event_id)
        self.assertIsNotNone(event); self.assertIsNotNone(context); self.assertEqual(event.event_type_code,"violence_fighting"); self.assertEqual(event.camera_id,CAMERA_ID); self.assertTrue(event.requires_attention); self.assertEqual(event.correlation_id,CORRELATION_ID); self.assertEqual(context.model_version_id,MODEL_ID); self.assertEqual(context.output_label,"fighting"); self.assertAlmostEqual(context.score_value,0.9957476258277893); self.assertAlmostEqual(context.event_threshold_snapshot,0.906); self.assertEqual(context.n_required_snapshot,3); self.assertEqual(context.history_window_size_snapshot,5); self.assertEqual(context.positive_count_snapshot,3)
    def test_nonqualifying_cannot_persist(self):
        with self.assertRaises(ViolenceEventPersistenceError): ViolenceEventPersistenceService(self.sessions).create_from_qualified_condition(evaluation=self.evaluation(False),requires_attention=True)
        with self.sessions() as session: self.assertEqual(len(list(session.scalars(select(Event)))),0)
    def test_unknown_camera_fails_without_partial_event(self):
        e=self.evaluation(True); bad=ViolenceConditionEvaluation(**{**e.__dict__,"camera_id":UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")})
        with self.assertRaises(ViolenceEventPersistenceError): ViolenceEventPersistenceService(self.sessions).create_from_qualified_condition(evaluation=bad,requires_attention=True)
        with self.sessions() as session: self.assertEqual(len(list(session.scalars(select(Event)))),0)
