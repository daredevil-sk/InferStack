from sqlalchemy import text
from app.core.database import engine

def register_model(name: str, version: str, storage_path: str, framework: str, accuracy: float):
    query = text("""
            INSERT INTO models (name, version, storage_path, framework, accuracy)
            VALUES (:name, :version, :storage_path, :framework, :accuracy)
        """)
    with engine.connect() as connection:
        connection.execute(query, {"name": name, "version": version, "storage_path": storage_path, "framework": framework, "accuracy": accuracy})
        connection.commit()

def get_model(name: str, version: str):
    query = text("""
            SELECT * FROM models
            WHERE name = :name AND version = :version
        """)
    with engine.connect() as connection:
        result = connection.execute(query, {"name": name, "version": version})
        row = result.fetchone()
        if row is None:
            return None
        return {
            "name": row.name,
            "version": row.version,
            "storage_path": row.storage_path
        }
    
def list_models():
    query = text("SELECT name, version, storage_path FROM models")
    with engine.connect() as connection:
        result = connection.execute(query)
        models = []
        for row in result:
            models.append({
                "name": row.name,
                "version": row.version,
                "storage_path": row.storage_path
            })
        return models

def get_latest_model(name):

    query = """
    SELECT name, version, storage_path
    FROM models
    WHERE name=:name
    ORDER BY created_at DESC
    LIMIT 1
    """

def delete_model(name: str, version: str):
    query = text("""
            DELETE FROM models
            WHERE name = :name AND version = :version
        """)
    with engine.connect() as connection:
        connection.execute(query, {"name": name, "version": version})
        connection.commit()