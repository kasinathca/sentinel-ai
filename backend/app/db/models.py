from __future__ import annotations
from datetime import datetime, timezone
from uuid import UUID, uuid4
from sqlalchemy import BigInteger,Boolean,CheckConstraint,DateTime,Float,ForeignKey,Integer,String,Text,UniqueConstraint,Uuid
from sqlalchemy.orm import Mapped,mapped_column,relationship
from .base import Base

def utc_now()->datetime: return datetime.now(timezone.utc)

class Camera(Base):
    __tablename__="cameras"
    id:Mapped[UUID]=mapped_column(Uuid(as_uuid=True),primary_key=True,default=uuid4)
    name:Mapped[str]=mapped_column(String(200),nullable=False)
    source_kind:Mapped[str]=mapped_column(String(50),nullable=False)
    enabled:Mapped[bool]=mapped_column(Boolean,nullable=False,default=True)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),nullable=False,default=utc_now)
    updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),nullable=False,default=utc_now,onupdate=utc_now)

class AIModel(Base):
    __tablename__="models"
    __table_args__=(UniqueConstraint("name","task_code",name="uq_models_name_task"),)
    id:Mapped[UUID]=mapped_column(Uuid(as_uuid=True),primary_key=True,default=uuid4)
    name:Mapped[str]=mapped_column(String(200),nullable=False)
    task_code:Mapped[str]=mapped_column(String(100),nullable=False)
    source_name:Mapped[str|None]=mapped_column(String(200),nullable=True)
    source_url:Mapped[str|None]=mapped_column(Text,nullable=True)
    license_name:Mapped[str|None]=mapped_column(String(200),nullable=True)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),nullable=False,default=utc_now)
    versions:Mapped[list["AIModelVersion"]]=relationship(back_populates="model")

class AIModelVersion(Base):
    __tablename__="model_versions"
    __table_args__=(UniqueConstraint("model_id","version_label",name="uq_model_versions_model_label"),)
    id:Mapped[UUID]=mapped_column(Uuid(as_uuid=True),primary_key=True)
    model_id:Mapped[UUID]=mapped_column(Uuid(as_uuid=True),ForeignKey("models.id",ondelete="RESTRICT"),nullable=False,index=True)
    version_label:Mapped[str]=mapped_column(String(200),nullable=False)
    experiment_id:Mapped[str|None]=mapped_column(String(200),nullable=True)
    artifact_reference:Mapped[str]=mapped_column(Text,nullable=False)
    artifact_sha256:Mapped[str|None]=mapped_column(String(64),nullable=True)
    framework_name:Mapped[str|None]=mapped_column(String(100),nullable=True)
    framework_version:Mapped[str|None]=mapped_column(String(100),nullable=True)
    base_model_reference:Mapped[str|None]=mapped_column(Text,nullable=True)
    dataset_registry_id:Mapped[str|None]=mapped_column(String(200),nullable=True)
    training_commit:Mapped[str|None]=mapped_column(String(64),nullable=True)
    status_code:Mapped[str]=mapped_column(String(50),nullable=False)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),nullable=False,default=utc_now)
    model:Mapped[AIModel]=relationship(back_populates="versions")

class ViolenceEventPolicy(Base):
    __tablename__="violence_event_policies"
    __table_args__=(
        CheckConstraint("event_threshold_value >= 0.0 AND event_threshold_value <= 1.0",name="threshold_range"),
        CheckConstraint("n_required > 0",name="n_required_positive"),
        CheckConstraint("history_window_size > 0",name="history_positive"),
        CheckConstraint("n_required <= history_window_size",name="n_not_greater_than_m"),
        CheckConstraint("stride_feature_steps > 0",name="stride_positive"),
        CheckConstraint("cooldown_ms IS NULL OR cooldown_ms >= 0",name="cooldown_nonnegative"),
    )
    id:Mapped[UUID]=mapped_column(Uuid(as_uuid=True),primary_key=True,default=uuid4)
    camera_id:Mapped[UUID|None]=mapped_column(Uuid(as_uuid=True),ForeignKey("cameras.id",ondelete="RESTRICT"),nullable=True,index=True)
    model_version_id:Mapped[UUID]=mapped_column(Uuid(as_uuid=True),ForeignKey("model_versions.id",ondelete="RESTRICT"),nullable=False,index=True)
    enabled:Mapped[bool]=mapped_column(Boolean,nullable=False,default=True)
    event_threshold_value:Mapped[float]=mapped_column(Float,nullable=False)
    score_semantics:Mapped[str]=mapped_column(Text,nullable=False)
    n_required:Mapped[int]=mapped_column(Integer,nullable=False)
    history_window_size:Mapped[int]=mapped_column(Integer,nullable=False)
    stride_feature_steps:Mapped[int]=mapped_column(Integer,nullable=False)
    cooldown_ms:Mapped[int|None]=mapped_column(BigInteger,nullable=True)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),nullable=False,default=utc_now)
    updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),nullable=False,default=utc_now,onupdate=utc_now)

class Event(Base):
    __tablename__="events"
    id:Mapped[UUID]=mapped_column(Uuid(as_uuid=True),primary_key=True,default=uuid4)
    event_type_code:Mapped[str]=mapped_column(String(100),nullable=False,index=True)
    camera_id:Mapped[UUID]=mapped_column(Uuid(as_uuid=True),ForeignKey("cameras.id",ondelete="RESTRICT"),nullable=False,index=True)
    rule_id:Mapped[UUID|None]=mapped_column(Uuid(as_uuid=True),nullable=True)
    occurred_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),nullable=False)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),nullable=False,default=utc_now)
    severity_code:Mapped[str|None]=mapped_column(String(50),nullable=True)
    requires_attention:Mapped[bool]=mapped_column(Boolean,nullable=False)
    lifecycle_status_code:Mapped[str|None]=mapped_column(String(50),nullable=True)
    correlation_id:Mapped[UUID|None]=mapped_column(Uuid(as_uuid=True),nullable=True)
    summary:Mapped[str|None]=mapped_column(Text,nullable=True)
    violence_context:Mapped["ViolenceEventContext|None"]=relationship(back_populates="event",uselist=False,cascade="all, delete-orphan")

class ViolenceEventContext(Base):
    __tablename__="violence_event_context"
    __table_args__=(
        CheckConstraint("score_value IS NULL OR (score_value >= 0.0 AND score_value <= 1.0)",name="score_range"),
        CheckConstraint("event_threshold_snapshot IS NULL OR (event_threshold_snapshot >= 0.0 AND event_threshold_snapshot <= 1.0)",name="threshold_snapshot_range"),
    )
    event_id:Mapped[UUID]=mapped_column(Uuid(as_uuid=True),ForeignKey("events.id",ondelete="CASCADE"),primary_key=True)
    model_version_id:Mapped[UUID]=mapped_column(Uuid(as_uuid=True),ForeignKey("model_versions.id",ondelete="RESTRICT"),nullable=False,index=True)
    output_label:Mapped[str]=mapped_column(String(100),nullable=False)
    score_value:Mapped[float|None]=mapped_column(Float,nullable=True)
    event_threshold_snapshot:Mapped[float|None]=mapped_column(Float,nullable=True)
    score_semantics:Mapped[str|None]=mapped_column(Text,nullable=True)
    window_started_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True),nullable=True)
    window_ended_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True),nullable=True)
    n_required_snapshot:Mapped[int|None]=mapped_column(Integer,nullable=True)
    history_window_size_snapshot:Mapped[int|None]=mapped_column(Integer,nullable=True)
    positive_count_snapshot:Mapped[int|None]=mapped_column(Integer,nullable=True)
    event:Mapped[Event]=relationship(back_populates="violence_context")
