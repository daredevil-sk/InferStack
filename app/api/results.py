from fastapi import APIRouter, HTTPException
from app.core.result_store import get_result

router = APIRouter(prefix="/results", tags=["results"])

@router.get("/{job_id}")
def fetch_result(job_id: str):
    result = get_result(job_id)
    print("DB RESULT:", result)
    if not result:
        return {"job_id": job_id, "status": "pending"}
    status = result["status"]
    if status == "failed":
        return {"status":"failed", "error":result["error"] if "error" in result else None}
    prediction = None
    if "prediction" in result:
        import ast
        prediction = ast.literal_eval(result["prediction"])
    return {
        "job_id": job_id,
        "result": result,
        "prediction": prediction,
        "status": "completed"
    }