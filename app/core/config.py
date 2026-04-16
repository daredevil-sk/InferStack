import os

USE_KAFKA = os.getenv("USE_KAFKA", "true").lower() == "true"
MODEL_DIR = os.getenv("MODEL_DIR", "models")
DB_URL = os.getenv("DB_URL", "mysql://root:root@db/model_registry")