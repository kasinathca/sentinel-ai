from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.cameras.service import create_camera, get_camera, list_cameras, update_camera
from app.db.session import get_session_factory


router = APIRouter(prefix="/api/v1/cameras", tags=["cameras"])


def get_db():
    session_factory = get_session_factory()
    with session_factory() as session:
        yield session


class CameraCreate(BaseModel):
    name: str
    source_kind: str
    enabled: bool = True


class CameraUpdate(BaseModel):
    name: str | None = None
    source_kind: str | None = None
    enabled: bool | None = None


@router.post("")
def create_camera_endpoint(
    payload: CameraCreate,
    session: Session = Depends(get_db),
):
    camera = create_camera(
        session,
        name=payload.name,
        source_kind=payload.source_kind,
        enabled=payload.enabled,
    )
    session.commit()
    session.refresh(camera)

    return {
        "data": {
            "id": str(camera.id),
            "name": camera.name,
            "source_kind": camera.source_kind,
            "enabled": camera.enabled,
            "created_at": camera.created_at,
            "updated_at": camera.updated_at,
        }
    }


@router.get("")
def list_camera_endpoint(
    enabled: bool | None = None,
    session: Session = Depends(get_db),
):
    cameras = list_cameras(session, enabled=enabled)

    return {
        "data": [
            {
                "id": str(camera.id),
                "name": camera.name,
                "source_kind": camera.source_kind,
                "enabled": camera.enabled,
                "created_at": camera.created_at,
                "updated_at": camera.updated_at,
            }
            for camera in cameras
        ],
        "meta": {
            "limit": len(cameras),
            "next_cursor": None,
            "has_more": False,
        },
    }


@router.get("/{camera_id}")
def get_camera_endpoint(
    camera_id: UUID,
    session: Session = Depends(get_db),
):
    camera = get_camera(session, camera_id)

    if camera is None:
        raise HTTPException(
            status_code=404,
            detail="Camera was not found.",
        )

    return {
        "data": {
            "id": str(camera.id),
            "name": camera.name,
            "source_kind": camera.source_kind,
            "enabled": camera.enabled,
            "created_at": camera.created_at,
            "updated_at": camera.updated_at,
        }
    }


@router.patch("/{camera_id}")
def update_camera_endpoint(
    camera_id: UUID,
    payload: CameraUpdate,
    session: Session = Depends(get_db),
):
    camera = update_camera(
        session,
        camera_id,
        name=payload.name,
        source_kind=payload.source_kind,
        enabled=payload.enabled,
    )

    if camera is None:
        raise HTTPException(
            status_code=404,
            detail="Camera was not found.",
        )

    session.commit()
    session.refresh(camera)

    return {
        "data": {
            "id": str(camera.id),
            "name": camera.name,
            "source_kind": camera.source_kind,
            "enabled": camera.enabled,
            "created_at": camera.created_at,
            "updated_at": camera.updated_at,
        }
    }