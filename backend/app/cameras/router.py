from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from app.cameras.service import create_camera, get_camera, list_cameras, update_camera
from app.cameras.constants import (
    DEMO_CAMERA_ID,
    DEMO_CAMERA_NAME,
    DEMO_CAMERA_SOURCE_KIND,
)
from app.demo.controller import DemoSourceState, VirtualCameraController
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


def _camera_health(camera, controller: VirtualCameraController | None) -> dict:
    if camera.id != DEMO_CAMERA_ID or controller is None:
        return {
            "state": "unknown",
            "last_frame_at": None,
            "last_health_check_at": None,
        }

    state = controller.snapshot().state
    if not camera.enabled:
        state = DemoSourceState.STOPPED
    health_state = {
        DemoSourceState.IDLE: "stopped",
        DemoSourceState.READY: "stopped",
        DemoSourceState.STARTING: "starting",
        DemoSourceState.PLAYING: "online",
        DemoSourceState.LOOP_RESTARTING: "online",
        DemoSourceState.STOPPED: "stopped",
        DemoSourceState.FAILED: "error",
    }[state]
    return {
        "state": health_state,
        "last_frame_at": controller.last_frame_at,
        "last_health_check_at": datetime.now(timezone.utc),
    }


def camera_to_dict(
    camera,
    *,
    controller: VirtualCameraController | None = None,
    include_timestamps: bool = True,
) -> dict:
    result = {
        "id": str(camera.id),
        "name": camera.name,
        "description": camera.description,
        "source_kind": camera.source_kind,
        "enabled": camera.enabled,
        # Only the configured demo camera has a process-local source health
        # signal. Other cameras remain unknown regardless of enabled status.
        "health": _camera_health(camera, controller),
    }
    if include_timestamps:
        result["created_at"] = _utc(camera.created_at)
        result["updated_at"] = _utc(camera.updated_at)
    return result


@router.post("", status_code=201)
def create_camera_endpoint(
    payload: CameraCreate,
    request: Request,
    session: Session = Depends(get_db),
):
    if payload.name.strip() == DEMO_CAMERA_NAME:
        raise HTTPException(
            status_code=409,
            detail="The DEMO-CAM-01 name is reserved for the canonical demo camera.",
        )
    camera = create_camera(
        session,
        name=payload.name,
        source_kind=payload.source_kind,
        description=payload.description,
        enabled=payload.enabled,
    )
    session.commit()
    session.refresh(camera)
    return {
        "data": camera_to_dict(
            camera, controller=request.app.state.demo_controller
        )
    }


@router.get("")
def list_camera_endpoint(
    request: Request,
    enabled: bool | None = None,
    session: Session = Depends(get_db),
):
    cameras = list_cameras(session, enabled=enabled)
    return {
        "data": [
            camera_to_dict(
                camera,
                controller=request.app.state.demo_controller,
                include_timestamps=False,
            )
            for camera in cameras
        ],
        "meta": {"limit": len(cameras), "next_cursor": None, "has_more": False},
    }


@router.get("/{camera_id}")
def get_camera_endpoint(
    camera_id: UUID, request: Request, session: Session = Depends(get_db)
):
    camera = get_camera(session, camera_id)
    if camera is None:
        raise HTTPException(status_code=404, detail="Camera was not found.")
    return {
        "data": camera_to_dict(
            camera, controller=request.app.state.demo_controller
        )
    }


@router.patch("/{camera_id}")
def update_camera_endpoint(
    camera_id: UUID,
    payload: CameraUpdate,
    request: Request,
    session: Session = Depends(get_db),
):
    changes = payload.model_dump(exclude_unset=True)
    camera = get_camera(session, camera_id)
    if camera is None:
        raise HTTPException(status_code=404, detail="Camera was not found.")

    requested_name = changes.get("name")
    if camera_id == DEMO_CAMERA_ID:
        if requested_name is not None and requested_name != DEMO_CAMERA_NAME:
            raise HTTPException(
                status_code=409,
                detail="The canonical demo camera name cannot be changed.",
            )
        requested_source_kind = changes.get("source_kind")
        if (
            requested_source_kind is not None
            and requested_source_kind != DEMO_CAMERA_SOURCE_KIND
        ):
            raise HTTPException(
                status_code=409,
                detail="The canonical demo camera source_kind cannot be changed.",
            )
    elif requested_name is not None and requested_name.strip() == DEMO_CAMERA_NAME:
        raise HTTPException(
            status_code=409,
            detail="The DEMO-CAM-01 name is reserved for the canonical demo camera.",
        )

    controller: VirtualCameraController = request.app.state.demo_controller
    sync_disable = camera_id == DEMO_CAMERA_ID and changes.get("enabled") is False
    previous_enabled = camera.enabled
    if sync_disable:
        # Serialize disable against Start so no request can begin replay between
        # the database check and controller shutdown.
        controller.set_enabled(False)

    try:
        camera = update_camera(session, camera_id, **changes)
        assert camera is not None
        if "description" in changes:
            camera.description = changes["description"]
        session.commit()
    except Exception:
        session.rollback()
        if sync_disable and previous_enabled:
            # Restore eligibility after a failed database update; stay stopped.
            controller.set_enabled(True)
        raise
    session.refresh(camera)
    if camera_id == DEMO_CAMERA_ID and changes.get("enabled") is True:
        controller.set_enabled(True)
    return {
        "data": camera_to_dict(
            camera, controller=request.app.state.demo_controller
        )
    }


@router.get("/{camera_id}/health")
def get_camera_health(
    camera_id: UUID, request: Request, session: Session = Depends(get_db)
):
    camera = get_camera(session, camera_id)
    if camera is None:
        raise HTTPException(status_code=404, detail="Camera was not found.")
    return {
        "data": {
            "camera_id": str(camera.id),
            "enabled": camera.enabled,
            **_camera_health(camera, request.app.state.demo_controller),
        }
    }


@router.get("/{camera_id}/stream")
def stream_demo_camera(
    camera_id: UUID,
    request: Request,
    session: Session = Depends(get_db),
):
    """Expose the canonical local demo source as an MJPEG multipart stream."""
    if request.client is None or request.client.host not in {
        "127.0.0.1",
        "::1",
        "testclient",
    }:
        raise HTTPException(
            status_code=403, detail="Camera stream is available only locally."
        )
    if camera_id != DEMO_CAMERA_ID:
        raise HTTPException(status_code=404, detail="Camera stream was not found.")
    camera = get_camera(session, camera_id)
    if camera is None:
        raise HTTPException(status_code=404, detail="Camera was not found.")
    if not camera.enabled:
        raise HTTPException(status_code=409, detail="Camera source is disabled.")
    controller: VirtualCameraController = request.app.state.demo_controller
    adapter = request.app.state.demo_replay_adapter
    if adapter is None or not hasattr(adapter, "wait_for_frame"):
        raise HTTPException(status_code=503, detail="Camera replay is unavailable.")
    snapshot = controller.snapshot()
    if snapshot.state not in {
        DemoSourceState.STARTING,
        DemoSourceState.PLAYING,
        DemoSourceState.LOOP_RESTARTING,
    }:
        raise HTTPException(status_code=409, detail="Camera source is not active.")

    def frames():
        sequence = 0
        while controller.snapshot().state in {
            DemoSourceState.STARTING,
            DemoSourceState.PLAYING,
            DemoSourceState.LOOP_RESTARTING,
        }:
            frame = adapter.wait_for_frame(sequence, timeout_seconds=1.0)
            if frame is None:
                continue
            sequence, jpeg = frame
            yield (
                b"--frame\r\nContent-Type: image/jpeg\r\nContent-Length: "
                + str(len(jpeg)).encode("ascii")
                + b"\r\n\r\n"
                + jpeg
                + b"\r\n"
            )

    return StreamingResponse(
        frames(),
        media_type="multipart/x-mixed-replace; boundary=frame",
        headers={"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff"},
    )
