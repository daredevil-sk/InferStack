import time
from kafka import KafkaProducer
import json
from kafka.admin import KafkaAdminClient, NewTopic

def create_topic():
    retries = 10
    for i in range(retries):
        try:
            admin = KafkaAdminClient(bootstrap_servers="kafka:9092")

            topic = NewTopic(
                name="inference-topic",
                num_partitions=1,
                replication_factor=1
            )

            admin.create_topics([topic])
            print("✅ Kafka topic created")
            return
        except Exception as e:
            print(f"⚠️ Kafka not ready (attempt {i+1}/{retries}):", e)
            time.sleep(3)
    print("❌ Failed to create Kafka topic after retries")
def create_producer():
    for _ in range(10):
        try:
            return KafkaProducer(
                bootstrap_servers='kafka:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
        except Exception as e:
            print("Kafka not ready, retrying...")
            time.sleep(2)
    raise Exception("Kafka not available")

producer = None

def get_producer():
    global producer
    if producer is None:
        producer = create_producer()
    return producer


def send_inference_request(data):
    producer = get_producer()
    producer.send("inference-topic", data)
    producer.flush()