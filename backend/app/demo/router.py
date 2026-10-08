from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy.orm import Session

from app.cameras.constants import DEMO_CAMERA_ID
from app.cameras.router import get_db
from app.db.models import Camera
from app.demo.clip_catalog import DemoCatalogError, DemoClipNotFound
from app.demo.controller import DemoControllerError, VirtualCameraController


def get_demo_controller(request: Request) -> VirtualCameraController:
    return request.app.state.demo_controller


def require_local_demo_access(request: Request) -> None:
    """Limit unauthenticated source controls to same-machine requests."""
    client = request.client
    if client is None or client.host not in {"127.0.0.1", "::1", "testclient"}:
        raise DemoControllerError(
            "FORBIDDEN", "Demo source controls are available only locally.", 403
        )


router = APIRouter(
    prefix="/api/v1/demo",
    tags=["demo source"],
    dependencies=[Depends(require_local_demo_access)],
)


class DemoSourceSelection(BaseModel):
    model_config = ConfigDict(extra="forbid")
    clip_id: str = Field(min_length=1)

    @field_validator("clip_id")
    @classmethod
    def strip_clip_id(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("clip_id must not be empty.")
        return normalized


@router.get("/clips")
def list_demo_clips(controller: VirtualCameraController = Depends(get_demo_controller)):
    try:
        clips = [clip.to_public_dict() for clip in controller.list_clips()]
        return {
            "data": clips,
            "meta": {"limit": len(clips), "next_cursor": None, "has_more": False},
        }
    except DemoCatalogError as exc:
        raise DemoControllerError(
            "SOURCE_CONFIGURATION_INVALID",
            "The approved demo clip catalog is unavailable or invalid.",
            503,
        ) from exc


@router.put("/source")
def select_demo_source(
    payload: DemoSourceSelection,
    controller: VirtualCameraController = Depends(get_demo_controller),
):
    try:
        return {"data": controller.select_source(payload.clip_id).to_public_dict()}
    except DemoClipNotFound as exc:
        raise DemoControllerError(
            "DEMO_CLIP_NOT_FOUND", "The requested demo clip is not registered.", 404
        ) from exc
    except DemoCatalogError as exc:
        raise DemoControllerError(
            "SOURCE_CONFIGURATION_INVALID",
            "The approved demo clip catalog is unavailable or invalid.",
            503,
        ) from exc


@router.post("/source/start")
def start_demo_source(
    controller: VirtualCameraController = Depends(get_demo_controller),
    session: Session = Depends(get_db),
):
    camera = session.get(Camera, DEMO_CAMERA_ID)
    if camera is None:
        raise DemoControllerError(
            "SOURCE_UNAVAILABLE", "The canonical demo camera is not initialized.", 503
        )
    return {"data": controller.start(enabled=camera.enabled).to_public_dict()}


@router.post("/source/stop")
def stop_demo_source(controller: VirtualCameraController = Depends(get_demo_controller)):
    return {"data": controller.stop().to_public_dict()}


@router.post("/source/restart")
def restart_demo_source(controller: VirtualCameraController = Depends(get_demo_controller)):
    return {"data": controller.restart().to_public_dict()}


@router.get("/source/status")
def demo_source_status(controller: VirtualCameraController = Depends(get_demo_controller)):
    return {"data": controller.snapshot().to_public_dict()}
