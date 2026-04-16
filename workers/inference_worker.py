import time
from kafka import KafkaConsumer
import json

from app.services.model_loader import load_model
from app.core.result_store import store_result  
from app.core.logger import get_logger

while True:
    try:
        consumer = KafkaConsumer(
            "inference-topic",
            bootstrap_servers="kafka:9092",
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            auto_offset_reset="earliest",
            group_id="inference-group"
        )
        print("Worker started...")
        break
    except Exception as e:
        print(f"Failed to connect to Kafka: {str(e)}. Retrying in 5 seconds...")
        time.sleep(5)

print("Worker started...")

for message in consumer:
    job = message.value

    try:
        job_id = job["job_id"]

        print("Processing:", job)

        model = load_model(job["model_name"], job["version"])
        prediction = model.predict([job["features"]]).tolist()

        store_result(job_id, "completed", prediction=prediction)

        print(f"[SUCCESS] {job_id} -> {prediction}")

    except Exception as e:
        job_id = job.get("job_id", "unknown")

        print(f"[FAILED] {job_id} -> {str(e)}")

        store_result(job_id, "failed", error=str(e))

logger = get_logger("worker")

logger.info(f"Processing job {job_id}")
logger.info(f"Prediction result: {prediction}")