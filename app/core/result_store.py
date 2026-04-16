from sqlalchemy import create_engine, text

engine = create_engine("mysql+pymysql://root:password@mysql:3306/model_registry")


def store_result(job_id, status, prediction=None, error=None):
    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO inference_results (job_id, status, prediction, error)
                VALUES (:job_id, :status, :prediction, :error)
                ON DUPLICATE KEY UPDATE
                status=:status, prediction=:prediction, error=:error
            """),
            {
                "job_id": job_id,
                "status": status,
                "prediction": str(prediction),
                "error": error
            }
        )
        conn.commit()


def get_result(job_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT status, prediction, error FROM inference_results WHERE job_id=:job_id"),
            {"job_id": job_id}
        ).fetchone()

        if not result:
            return None

        return {
            "status": result[0],
            "prediction": result[1],
            "error": result[2]
        }