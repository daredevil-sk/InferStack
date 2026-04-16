from fastapi import APIRouter, HTTPException
from uuid import uuid4

from app.schemas.predict import PredictRequest
from app.core.metrics import prediction_counter
from app.core.logger import get_logger
from app.core.config import USE_KAFKA
from app.services.model_loader import load_model
from app.core.kafka_producer import send_inference_request
from app.core.result_store import store_result

logger = get_logger("api")
router = APIRouter()

@router.post("/predict")
def predict(payload: PredictRequest):
    try:
        job_id = str(uuid4())

        job = {
            "job_id": job_id,
            "model_name": payload.model_name,
            "version": payload.version,
            "features": payload.features
        }
        store_result(job_id, "pending")  # Store initial status
        # send to Kafka
        if USE_KAFKA:
            send_inference_request(job)
        else:
            try:
                model = load_model(payload.model_name, payload.version)
                prediction = model.predict([payload.features]).tolist()
                store_result(job_id, "completed", prediction=prediction)
            except Exception as e:
                store_result(job_id, "failed", error=str(e))
                raise HTTPException(status_code=500, detail=str(e))
        # metrics + logging
        prediction_counter.inc()
        logger.info(f"Queued prediction {job_id}: {payload.model_name}:{payload.version}")

        return {
            "job_id": job_id,
            "status": "queued"
        }

    except Exception as e:
        logger.error(f"Error occurred while processing prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))