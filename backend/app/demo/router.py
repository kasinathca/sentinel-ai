from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy.orm import Session

from app.ai_integration.constants import (
    LIVE_M_HISTORY,
    LIVE_N_REQUIRED,
    LIVE_THRESHOLD,
    MODEL_VERSION_ID,
    SCORE_SEMANTICS,
)
from app.cameras.constants import DEMO_CAMERA_ID
from app.cameras.router import get_db
from app.db.models import Camera
from app.demo.clip_catalog import DemoCatalogError, DemoClipNotFound, DemoClipNotReady
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
            "meta": {
                "limit": len(clips),
                "next_cursor": None,
                "has_more": False,
                "ready": sum(clip["state"] == "ready" for clip in clips),
                "preparing": sum(
                    clip["state"] in {"waiting_for_file", "validating", "transcoding"}
                    for clip in clips
                ),
                "rejected": sum(clip["state"] in {"rejected", "failed"} for clip in clips),
            },
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
    except DemoClipNotReady as exc:
        raise DemoControllerError(
            "DEMO_CLIP_NOT_READY",
            f"The requested demo video is not ready ({exc.state}).",
            409,
        ) from exc
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
def demo_source_status(
    request: Request,
    controller: VirtualCameraController = Depends(get_demo_controller),
):
    data = controller.snapshot().to_public_dict()
    orchestrator = request.app.state.demo_ai_orchestrator
    data["ai"] = (
        orchestrator.status().to_public_dict()
        if orchestrator is not None
        else {
            "state": "unavailable",
            "source_session_id": None,
            "latest_score": None,
            "latest_score_positive": False,
            "history_count": 0,
            "current_history_count": 0,
            "positive_count": 0,
            "current_positive_count": 0,
            "complete_history": False,
            "candidate_condition": False,
            "current_candidate_condition": False,
            "event_id": None,
            "session_event_id": None,
            "processed_windows": 0,
            "processed_windows_total": 0,
            "positive_windows_total": 0,
            "analyzed_passes": 0,
            "max_positive_count_observed_in_any_5_window": 0,
            "ever_qualified": False,
            "first_qualified_at": None,
            "session_violence_detected": False,
            "error": "AI orchestration is not configured.",
            "model_version_id": MODEL_VERSION_ID,
            "threshold": LIVE_THRESHOLD,
            "n_required": LIVE_N_REQUIRED,
            "m_history": LIVE_M_HISTORY,
            "criterion": f"{LIVE_N_REQUIRED}-of-{LIVE_M_HISTORY}",
            "score_semantics": SCORE_SEMANTICS,
        }
    )
    return {"data": data}
