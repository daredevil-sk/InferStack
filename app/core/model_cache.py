import joblib

model_cache = {}

def load_model(path):
    if path in model_cache:
        return model_cache[path]
    model = joblib.load(path)
    model_cache[path] = model
    return model