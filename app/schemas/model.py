from pydantic import BaseModel

class ModelRegisterRequest(BaseModel):
    name: str
    version: str
    framework: str
    accuracy: float