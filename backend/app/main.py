from fastapi import FastAPI

from app.core.config import SETTINGS
from app.health.router import router as health_router


def create_app() -> FastAPI:
    application = FastAPI(
        title="Sentinel AI API",
        version=SETTINGS.service_version,
    )
    application.include_router(health_router)
    return application


app = create_app()
