from fastapi import APIRouter, HTTPException, Request, UploadFile, File, Form
from pydantic import BaseModel
from app.schemas.model import ModelRegisterRequest
from app.services.model_registry import register_model, get_model, list_models, get_latest_model, delete_model
from app.core.database import engine
from app.db.models import models
import os
import shutil

router = APIRouter()
'''
@router.post("/register")
def register(request: ModelRegisterRequest):    
    try:
        register_model(request.name, request.version, request.storage_path, request.framework, request.accuracy)
        return {"message": "Model registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    '''

@router.get("/get")
def get(name: str, version: str):
    model = get_model(name, version)
    if model:
        return model
    else:
        raise HTTPException(status_code=404, detail="Model not found")

@router.get("/list")
def list_all():
    return list_models()

@router.get("/latest")
def get_latest(name: str):
    model = get_latest_model(name)
    if model:
        return model
    else:
        raise HTTPException(status_code=404, detail="Model not found")
    
@router.delete("/delete")
def delete(name: str, version: str):
    try:
        delete_model(name, version)
        return {"message": "Model deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

MODEL_DIR = "/models"
class ModelRegister(BaseModel):
    name: str
    version: str
    framework: str
    accuracy: float

@router.post("/register")
def register_model(payload: ModelRegister):
    try:
        print("REGISTER MODEL CALLED:", payload)

        filename = f"{payload.name}_{payload.version}.pkl"
        file_path = f"/models/{filename}"

        # check file exists
        if not os.path.exists(file_path):
            print("❌ Model file not found:", file_path)
            raise HTTPException(status_code=400, detail="Model file not found on server")

        with engine.begin() as conn:
            conn.execute(
                models.insert().values(
                    name=payload.name,
                    version=payload.version,
                    storage_path=file_path,
                    framework=payload.framework,
                    accuracy=payload.accuracy
                )
            )
        print("✅ Model registered in DB:", payload.name, payload.version)
        return {"message": "Model registered successfully"}

    except Exception as e:
        print("❌ ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))