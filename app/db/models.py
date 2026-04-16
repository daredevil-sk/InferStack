from sqlalchemy import Column, Integer, String, Float, Text, Table
import sqlalchemy
from app.db.base import metadata

models = Table(
    "models",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),    
    Column("version", String(50)),
    Column("storage_path", Text),
    Column("framework", String(50)),
    Column("accuracy", Float),
    sqlalchemy.UniqueConstraint("name", "version", name="uix_name_version")
)

inference_results = Table(
    "inference_results",
    metadata,
    Column("job_id", String(255), primary_key=True),
    Column("status", String(50)),
    Column("prediction", Text),
    Column("error", Text)
)