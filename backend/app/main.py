from fastapi import FastAPI

from app.core.config import SETTINGS
from app.health.router import router as health_router
from app.cameras.router import router as cameras_router


def create_app() -> FastAPI:
    application = FastAPI(
        title="Sentinel AI API",
        version=SETTINGS.service_version,
    )
    application.include_router(health_router)
    application.include_router(cameras_router)
    return application


app = create_app()