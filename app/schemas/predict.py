from pydantic import BaseModel
from typing import List

class PredictRequest(BaseModel):
    model_name: str
    version: str
    features: List[float]


class PredictResponse(BaseModel):
    model: str
    version: str
    prediction: List[int]