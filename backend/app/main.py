from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.responses import JSONResponse, Response

from app.core.config import SETTINGS
from app.health.router import router as health_router
from app.cameras.router import router as cameras_router
from app.ai_integration.router import router as ai_router
from app.events.router import router as events_router
from app.demo.clip_catalog import DemoClipCatalog
from app.demo.controller import DemoControllerError, VirtualCameraController
from app.demo.router import router as demo_router
from app.demo.ffmpeg_replay import FFmpegReplayAdapter


def create_app(demo_controller: VirtualCameraController | None = None) -> FastAPI:
    controller = demo_controller or VirtualCameraController(
        catalog_factory=DemoClipCatalog.from_environment,
        replay_adapter=FFmpegReplayAdapter.from_environment(),
    )

    @asynccontextmanager
    async def lifespan(application: FastAPI):
        try:
            yield
        finally:
            application.state.demo_controller.stop()

    application = FastAPI(
        title="Sentinel AI API",
        version=SETTINGS.service_version,
        lifespan=lifespan,
    )

    application.include_router(health_router)
    application.include_router(cameras_router)
    application.include_router(ai_router)
    application.include_router(events_router)
    application.include_router(demo_router)
    application.state.demo_controller = controller
    application.state.demo_replay_adapter = controller.replay_adapter

    @application.exception_handler(DemoControllerError)
    async def demo_controller_error_handler(
        request: Request, exc: DemoControllerError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.http_status,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "details": {},
                }
            },
        )

    @application.exception_handler(RequestValidationError)
    async def request_validation_handler(
        request: Request, exc: RequestValidationError
    ) -> Response:
        if not request.url.path.startswith("/api/v1/demo/"):
            return await request_validation_exception_handler(request, exc)
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Request validation failed.",
                    "details": {
                        "fields": [
                            {
                                "path": ".".join(str(part) for part in error["loc"]),
                                "code": error["type"],
                                "message": error["msg"],
                            }
                            for error in exc.errors()
                        ]
                    },
                }
            },
        )

    return application


app = create_app()
