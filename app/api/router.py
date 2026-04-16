from fastapi import APIRouter
from app.api.inference import router as inference_router
from app.api.models import router as models_router
from app.api.health import router as health_router

api_router = APIRouter()
api_router.include_router(health_router)

api_router.include_router(inference_router, prefix="/inference", tags=["inference"])
api_router.include_router(models_router, prefix="/models", tags=["models"])
