from __future__ import annotations
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker
from app.db.models import AIModel,AIModelVersion,ViolenceEventPolicy
from .model_registry import ModelRegistry,UnknownModelVersionError,ViolenceModelVersion
class DatabaseModelRegistry(ModelRegistry):
    # Phase 2M supports the frozen global MVP policy only (camera_id IS NULL).
    def __init__(self,session_factory:sessionmaker[Session])->None: self.session_factory=session_factory
    def get_violence_model_version(self,model_version_id:UUID)->ViolenceModelVersion:
        with self.session_factory() as session:
            row=session.execute(select(AIModelVersion,AIModel).join(AIModel,AIModel.id==AIModelVersion.model_id).where(AIModelVersion.id==model_version_id)).one_or_none()
            if row is None: raise UnknownModelVersionError(str(model_version_id))
            version,model=row
            policies=list(session.scalars(select(ViolenceEventPolicy).where(ViolenceEventPolicy.model_version_id==model_version_id,ViolenceEventPolicy.enabled.is_(True),ViolenceEventPolicy.camera_id.is_(None)).order_by(ViolenceEventPolicy.created_at.asc())))
            if len(policies)!=1: raise RuntimeError(f"Expected exactly one enabled global frozen violence policy for model version {model_version_id}; found {len(policies)}.")
            p=policies[0]
            return ViolenceModelVersion(id=version.id,experiment_id=version.experiment_id or "",version_label=version.version_label,task=model.task_code,checkpoint_sha256=version.artifact_sha256 or "",score_semantics=p.score_semantics,event_threshold_value=p.event_threshold_value,n_required=p.n_required,history_window_size=p.history_window_size,stride_feature_steps=p.stride_feature_steps,window_feature_steps=1)
