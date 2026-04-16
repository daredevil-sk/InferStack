from fastapi import APIRouter
from sqlalchemy import text
from app.core.database import engine

from kafka import KafkaAdminClient

router = APIRouter()
 

@router.get("/health/db")
def health_db():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


@router.get("/health/kafka")
def health_kafka():
    try:
        admin = KafkaAdminClient(bootstrap_servers="kafka:9092")
        topics = admin.list_topics()
        return {"status": "healthy", "topics": list(topics)}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}