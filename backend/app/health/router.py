from fastapi import APIRouter
from app.core.config import SETTINGS
router=APIRouter(prefix="/api/v1",tags=["health"])
@router.get("/health")
def health()->dict:
    return {"data":{"status":"ok","service":SETTINGS.service_name,"version":SETTINGS.service_version}}
