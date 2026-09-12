from __future__ import annotations
from dataclasses import dataclass
from uuid import UUID, uuid4
from sqlalchemy.orm import Session, sessionmaker
from app.db.models import AIModelVersion,Camera,Event,ViolenceEventContext
from app.events.violence_conditions import ViolenceConditionEvaluation
class ViolenceEventPersistenceError(ValueError): pass
@dataclass(frozen=True)
class PersistedViolenceEvent:
    event_id:UUID; camera_id:UUID; model_version_id:UUID; correlation_id:UUID; occurred_at_iso:str
class ViolenceEventPersistenceService:
    # This service does not decide duplicate/cooldown/retrigger behavior.
    EVENT_TYPE="violence_fighting"; OUTPUT_LABEL="fighting"
    def __init__(self,session_factory:sessionmaker[Session])->None: self.session_factory=session_factory
    def create_from_qualified_condition(self,*,evaluation:ViolenceConditionEvaluation,requires_attention:bool)->PersistedViolenceEvent:
        if not evaluation.candidate_condition: raise ViolenceEventPersistenceError("Cannot persist a violence event from a non-qualifying condition.")
        if not evaluation.complete_history: raise ViolenceEventPersistenceError("Cannot persist a violence event before the full N-of-M history exists.")
        event_id=uuid4()
        with self.session_factory.begin() as session:
            if session.get(Camera,evaluation.camera_id) is None: raise ViolenceEventPersistenceError(f"Camera does not exist: {evaluation.camera_id}")
            if session.get(AIModelVersion,evaluation.model_version_id) is None: raise ViolenceEventPersistenceError(f"Model version does not exist: {evaluation.model_version_id}")
            session.add(Event(id=event_id,event_type_code=self.EVENT_TYPE,camera_id=evaluation.camera_id,rule_id=None,occurred_at=evaluation.window_ended_at,severity_code=None,requires_attention=bool(requires_attention),lifecycle_status_code=None,correlation_id=evaluation.correlation_id,summary=None))
            session.add(ViolenceEventContext(event_id=event_id,model_version_id=evaluation.model_version_id,output_label=self.OUTPUT_LABEL,score_value=evaluation.score,event_threshold_snapshot=evaluation.threshold_snapshot,score_semantics=evaluation.score_semantics,window_started_at=evaluation.window_started_at,window_ended_at=evaluation.window_ended_at,n_required_snapshot=evaluation.n_required_snapshot,history_window_size_snapshot=evaluation.m_history_snapshot,positive_count_snapshot=evaluation.positive_count))
        return PersistedViolenceEvent(event_id=event_id,camera_id=evaluation.camera_id,model_version_id=evaluation.model_version_id,correlation_id=evaluation.correlation_id,occurred_at_iso=evaluation.window_ended_at.isoformat())
