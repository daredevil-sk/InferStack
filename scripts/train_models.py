from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

os.makedirs("models", exist_ok=True)

# Load dataset
X, y = load_iris(return_X_y=True)

# Train model
model = RandomForestClassifier().fit(X, y)

# Save model
joblib.dump(model, "models/iris_v1.pkl")

print("Model saved as models/iris_v1.pkl")

print(X.head())