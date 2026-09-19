from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Event, ViolenceEventContext
from app.db.session import get_session_factory


router = APIRouter(
    prefix="/api/v1/events",
    tags=["events"],
)


def get_db():
    session_factory = get_session_factory()

    with session_factory() as session:
        yield session


def event_to_dict(
    event: Event,
    context: ViolenceEventContext | None,
) -> dict:
    return {
        "id": str(event.id),
        "event_type_code": event.event_type_code,
        "camera_id": str(event.camera_id),
        "rule_id": str(event.rule_id) if event.rule_id else None,
        "occurred_at": event.occurred_at,
        "created_at": event.created_at,
        "severity_code": event.severity_code,
        "requires_attention": event.requires_attention,
        "lifecycle_status_code": event.lifecycle_status_code,
        "correlation_id": (
            str(event.correlation_id)
            if event.correlation_id
            else None
        ),
        "summary": event.summary,
        "violence_context": (
            {
                "model_version_id": str(context.model_version_id),
                "output_label": context.output_label,
                "score_value": context.score_value,
                "event_threshold_snapshot": (
                    context.event_threshold_snapshot
                ),
                "score_semantics": context.score_semantics,
                "window_started_at": context.window_started_at,
                "window_ended_at": context.window_ended_at,
                "n_required_snapshot": context.n_required_snapshot,
                "history_window_size_snapshot": (
                    context.history_window_size_snapshot
                ),
                "positive_count_snapshot": (
                    context.positive_count_snapshot
                ),
            }
            if context
            else None
        ),
    }


@router.get("")
def list_events(
    session: Session = Depends(get_db),
):
    statement = (
        select(Event, ViolenceEventContext)
        .outerjoin(
            ViolenceEventContext,
            ViolenceEventContext.event_id == Event.id,
        )
        .order_by(Event.occurred_at.desc(), Event.id.desc())
    )

    rows = session.execute(statement).all()

    return {
        "data": [
            event_to_dict(event, context)
            for event, context in rows
        ],
        "meta": {
            "limit": len(rows),
            "next_cursor": None,
            "has_more": False,
        },
    }


@router.get("/{event_id}")
def get_event(
    event_id: UUID,
    session: Session = Depends(get_db),
):
    statement = (
        select(Event, ViolenceEventContext)
        .outerjoin(
            ViolenceEventContext,
            ViolenceEventContext.event_id == Event.id,
        )
        .where(Event.id == event_id)
    )

    row = session.execute(statement).one_or_none()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Event was not found.",
        )

    event, context = row

    return {
        "data": event_to_dict(event, context)
    }