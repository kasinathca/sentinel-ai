from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from app.cameras.service import create_camera, get_camera, list_cameras, update_camera
from app.db.session import get_session_factory


router = APIRouter(prefix="/api/v1/cameras", tags=["cameras"])


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def get_db():
    session_factory = get_session_factory()
    with session_factory() as session:
        yield session


class CameraCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=1, max_length=200)
    source_kind: str = Field(min_length=1, max_length=50)
    description: str | None = None
    enabled: bool = True


class CameraUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str | None = Field(default=None, min_length=1, max_length=200)
    source_kind: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = None
    enabled: bool | None = None


def camera_to_dict(camera, *, include_timestamps: bool = True) -> dict:
    result = {
        "id": str(camera.id),
        "name": camera.name,
        "description": camera.description,
        "source_kind": camera.source_kind,
        "enabled": camera.enabled,
        # There is no health measurement subsystem yet. In particular, an
        # enabled camera is not evidence that its source is online.
        "health": {
            "state": "unknown",
            "last_frame_at": None,
            "last_health_check_at": None,
        },
    }
    if include_timestamps:
        result["created_at"] = _utc(camera.created_at)
        result["updated_at"] = _utc(camera.updated_at)
    return result


@router.post("", status_code=201)
def create_camera_endpoint(payload: CameraCreate, session: Session = Depends(get_db)):
    camera = create_camera(
        session,
        name=payload.name,
        source_kind=payload.source_kind,
        description=payload.description,
        enabled=payload.enabled,
    )
    session.commit()
    session.refresh(camera)
    return {"data": camera_to_dict(camera)}


@router.get("")
def list_camera_endpoint(
    enabled: bool | None = None,
    session: Session = Depends(get_db),
):
    cameras = list_cameras(session, enabled=enabled)
    return {
        "data": [camera_to_dict(camera, include_timestamps=False) for camera in cameras],
        "meta": {"limit": len(cameras), "next_cursor": None, "has_more": False},
    }


@router.get("/{camera_id}")
def get_camera_endpoint(camera_id: UUID, session: Session = Depends(get_db)):
    camera = get_camera(session, camera_id)
    if camera is None:
        raise HTTPException(status_code=404, detail="Camera was not found.")
    return {"data": camera_to_dict(camera)}


@router.patch("/{camera_id}")
def update_camera_endpoint(
    camera_id: UUID,
    payload: CameraUpdate,
    session: Session = Depends(get_db),
):
    changes = payload.model_dump(exclude_unset=True)
    camera = update_camera(session, camera_id, **changes)
    if camera is None:
        raise HTTPException(status_code=404, detail="Camera was not found.")
    if "description" in changes:
        camera.description = changes["description"]
    session.commit()
    session.refresh(camera)
    return {"data": camera_to_dict(camera)}


@router.get("/{camera_id}/health")
def get_camera_health(camera_id: UUID, session: Session = Depends(get_db)):
    camera = get_camera(session, camera_id)
    if camera is None:
        raise HTTPException(status_code=404, detail="Camera was not found.")
    return {
        "data": {
            "camera_id": str(camera.id),
            "enabled": camera.enabled,
            "state": "unknown",
            "last_frame_at": None,
            "last_health_check_at": None,
        }
    }
