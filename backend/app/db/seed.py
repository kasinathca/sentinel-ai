from __future__ import annotations
from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker
from app.ai_integration.constants import LIVE_M_HISTORY,LIVE_N_REQUIRED,LIVE_STRIDE_FEATURE_STEPS,LIVE_THRESHOLD,MODEL_CHECKPOINT_SHA256,MODEL_EXPERIMENT_ID,MODEL_VERSION_ID,MODEL_VERSION_LABEL,SCORE_SEMANTICS,VIOLENCE_TASK
from app.cameras.constants import (
    DEMO_CAMERA_DESCRIPTION,
    DEMO_CAMERA_ID,
    DEMO_CAMERA_NAME,
    DEMO_CAMERA_SOURCE_KIND,
)
from .models import AIModel,AIModelVersion,Camera,ViolenceEventPolicy
MODEL_FAMILY_ID=UUID("9edda127-a823-5299-9a1b-4e7839c07418")
GLOBAL_VIOLENCE_POLICY_ID=UUID("d3851e34-6edd-59c9-9643-453ec0820312")
def seed_frozen_violence_model(session_factory:sessionmaker[Session])->None:
    now=datetime.now(timezone.utc)
    with session_factory.begin() as session:
        model=session.get(AIModel,MODEL_FAMILY_ID)
        if model is None:
            session.add(AIModel(id=MODEL_FAMILY_ID,name="sentinel-violence-temporal",task_code=VIOLENCE_TASK,source_name="Sentinel AI",source_url=None,license_name=None,created_at=now))
        version_id=UUID(MODEL_VERSION_ID)
        version=session.get(AIModelVersion,version_id)
        if version is None:
            session.add(AIModelVersion(id=version_id,model_id=MODEL_FAMILY_ID,version_label=MODEL_VERSION_LABEL,experiment_id=MODEL_EXPERIMENT_ID,artifact_reference="external://sentinel_temporal/artifacts/best_model.pt",artifact_sha256=MODEL_CHECKPOINT_SHA256,framework_name="PyTorch",framework_version="2.13.0+cu130",base_model_reference=None,dataset_registry_id="DATA-DERIVED-XD-FIGHTING-BINARY-V1",training_commit=None,status_code="approved",created_at=now))
        policy=session.get(ViolenceEventPolicy,GLOBAL_VIOLENCE_POLICY_ID)
        if policy is None:
            session.add(ViolenceEventPolicy(id=GLOBAL_VIOLENCE_POLICY_ID,camera_id=None,model_version_id=version_id,enabled=True,event_threshold_value=LIVE_THRESHOLD,score_semantics=SCORE_SEMANTICS,n_required=LIVE_N_REQUIRED,history_window_size=LIVE_M_HISTORY,stride_feature_steps=LIVE_STRIDE_FEATURE_STEPS,cooldown_ms=None,created_at=now,updated_at=now))
        else:
            expected={"model_version_id":version_id,"camera_id":None,"enabled":True,"event_threshold_value":LIVE_THRESHOLD,"score_semantics":SCORE_SEMANTICS,"n_required":LIVE_N_REQUIRED,"history_window_size":LIVE_M_HISTORY,"stride_feature_steps":LIVE_STRIDE_FEATURE_STEPS,"cooldown_ms":None}
            for field,value in expected.items():
                if getattr(policy,field)!=value: raise RuntimeError(f"Existing frozen violence policy mismatch: {field}")


def seed_demo_camera(session_factory: sessionmaker[Session]) -> None:
    """Insert the stable academic demo camera without rewriting existing rows."""
    with session_factory.begin() as session:
        canonical = session.get(Camera, DEMO_CAMERA_ID)
        same_name = list(
            session.scalars(select(Camera).where(Camera.name == DEMO_CAMERA_NAME))
        )

        if canonical is not None:
            if canonical.name != DEMO_CAMERA_NAME:
                raise RuntimeError(
                    "Canonical demo camera identity conflict: the canonical UUID "
                    "is assigned to a different camera name."
                )
            if canonical.source_kind != DEMO_CAMERA_SOURCE_KIND:
                raise RuntimeError(
                    "Canonical demo camera identity conflict: DEMO-CAM-01 has a "
                    "non-canonical source_kind."
                )
            if any(camera.id != DEMO_CAMERA_ID for camera in same_name):
                raise RuntimeError(
                    "Canonical demo camera identity conflict: DEMO-CAM-01 exists "
                    "with a non-canonical UUID."
                )
            return

        if same_name:
            raise RuntimeError(
                "Canonical demo camera identity conflict: DEMO-CAM-01 exists "
                "with a non-canonical UUID."
            )

        session.add(
            Camera(
                id=DEMO_CAMERA_ID,
                name=DEMO_CAMERA_NAME,
                description=DEMO_CAMERA_DESCRIPTION,
                source_kind=DEMO_CAMERA_SOURCE_KIND,
                enabled=True,
            )
        )
