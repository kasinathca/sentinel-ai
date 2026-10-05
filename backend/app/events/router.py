from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import AIModelVersion, Camera, Event, ViolenceEventContext
from app.db.session import get_session_factory


router = APIRouter(prefix="/api/v1/events", tags=["events"])


def _utc(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def get_db():
    session_factory = get_session_factory()
    with session_factory() as session:
        yield session


def event_to_dict(
    event: Event,
    camera: Camera,
    context: ViolenceEventContext | None,
    model_version: AIModelVersion | None,
) -> dict:
    public_context: dict = {}
    if context is not None:
        version = model_version
        public_context = {
            "model_version": (
                {
                    "id": str(version.id),
                    "name": version.model.name,
                    "version": version.version_label,
                }
                if version is not None
                else {"id": str(context.model_version_id), "name": None, "version": None}
            ),
            "output_label": context.output_label,
            "score": context.score_value,
            "event_threshold": context.event_threshold_snapshot,
            "score_semantics": context.score_semantics,
            "window_started_at": _utc(context.window_started_at),
            "window_ended_at": _utc(context.window_ended_at),
        }

    return {
        "id": str(event.id),
        "event_type": event.event_type_code,
        "camera": {"id": str(camera.id), "name": camera.name},
        "occurred_at": _utc(event.occurred_at),
        "created_at": _utc(event.created_at),
        "requires_attention": event.requires_attention,
        "severity": event.severity_code,
        "status": event.lifecycle_status_code,
        "acknowledgement": {
            "acknowledged": False,
            "acknowledged_by": [],
            "first_acknowledged_at": None,
        },
        # No evidence rows/jobs are implemented, so all counts are truthfully 0.
        "evidence": {"available_count": 0, "pending_count": 0, "failed_count": 0},
        "context": public_context,
    }


def _event_rows(session: Session, event_id: UUID | None = None):
    statement = (
        select(Event, Camera, ViolenceEventContext, AIModelVersion)
        .join(Camera, Camera.id == Event.camera_id)
        .outerjoin(ViolenceEventContext, ViolenceEventContext.event_id == Event.id)
        .outerjoin(AIModelVersion, AIModelVersion.id == ViolenceEventContext.model_version_id)
    )
    if event_id is not None:
        statement = statement.where(Event.id == event_id)
    else:
        statement = statement.order_by(Event.occurred_at.desc(), Event.id.desc())
    return session.execute(statement).all()


@router.get("")
def list_events(session: Session = Depends(get_db)):
    rows = _event_rows(session)
    return {
        "data": [event_to_dict(event, camera, context, version) for event, camera, context, version in rows],
        "meta": {"limit": len(rows), "next_cursor": None, "has_more": False},
    }


@router.get("/{event_id}")
def get_event(event_id: UUID, session: Session = Depends(get_db)):
    row = next(iter(_event_rows(session, event_id)), None)
    if row is None:
        raise HTTPException(status_code=404, detail="Event was not found.")
    event, camera, context, version = row
    return {"data": event_to_dict(event, camera, context, version)}
