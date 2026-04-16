from fastapi import APIRouter
from app.services.model_loader import _loaded_models

router = APIRouter(prefix="/system")

@router.get("/cache")
def cache_status():
    return {
        "loaded_models": list(_loaded_models.keys()),
        "count": len(_loaded_models)
    }