import time
from sqlalchemy.exc import OperationalError
from app.db.base import metadata
from app.core.database import engine
from app.db.models import models, inference_results
def init_db(retries=10, delay=3):
    for i in range(retries):
        try:
            print(f"⏳ Trying DB connection ({i+1}/{retries})...")

            with engine.connect() as conn:
                metadata.create_all(bind=engine)

            print("✅ DB ready + tables created")
            return

        except OperationalError as e:
            print(f"❌ DB not ready: {e}")
            time.sleep(delay)

    raise Exception("❌ DB never became ready")