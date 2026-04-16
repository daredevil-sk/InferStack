import logging
from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import USE_KAFKA
from app.services.model_loader import load_model
from app.api.results import router as results_router
import time
from app.services.model_registry import list_models
from sqlalchemy import text
from app.core.database import engine
from app.core.kafka_producer import create_topic
from sqlalchemy.exc import OperationalError
from app.db.init_db import init_db
from app.core.logger import get_logger

logger = get_logger("api")

logger.info("Prediction requested")

def seed_models():
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM models WHERE name='iris' AND version='v1'")
        ).fetchone()

        if not result:
            conn.execute(text("""
                INSERT INTO models (name, version, storage_path)
                VALUES ('iris', 'v1', '/models/iris_v1.pkl')
            """))
            conn.commit()

def safe_seed_models():
    retries = 10
    for i in range(retries):
        try:
            seed_models()
            print("✅ DB seeded")
            return
        except OperationalError as e:
            print(f"⚠️ MySQL not ready (attempt {i+1}/{retries}):", e)
            time.sleep(3)

    print("❌ Failed to connect to MySQL after retries")

def preload_models():
    try:
        models = list_models()
        print("Models loaded:", models)
    except Exception as e:
        print("Failed to preload models:", e)

logging.basicConfig(level=logging.INFO)
app = FastAPI(
    title="ML Model Serving Platform",
    version="1.0"
)

app.include_router(api_router)
app.include_router(results_router)

@app.get("/")
def home():
    return {"message": "ML Model Serving API running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.on_event("startup")
def startup_event():
    if USE_KAFKA:
        try:
            create_topic()
        except Exception as e:
            print("Kafka init failed, continuing:", e)
    init_db()
    safe_seed_models()
    preload_models()