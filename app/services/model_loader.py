import joblib
from threading import Lock
from app.services.model_registry import get_model

_loaded_models = {}
lock = Lock()

def load_model(model_name: str, version: str):

    key = f"{model_name}:{version}"
    if key in _loaded_models:
        return _loaded_models[key]

    with lock:
        if key in _loaded_models:
            return _loaded_models[key]
        model_info = get_model(model_name, version)
        if model_info is None:
            raise ValueError("Model not registered")
        path = model_info["storage_path"]
        model = joblib.load(path)
        _loaded_models[key] = model
        return model