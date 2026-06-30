import joblib
import json
import numpy as np
import os

MODEL_PATH = os.path.join("artifacts", "loan_model.joblib")
SCALER_PATH = os.path.join("artifacts", "loan_scaler.joblib")
METRICS_PATH = os.path.join("artifacts", "loan_metrics.json")

def load_model():
    return joblib.load(MODEL_PATH)

def load_scaler():
    return joblib.load(SCALER_PATH)

def load_feature_columns():
    with open(METRICS_PATH) as f:
        metrics = json.load(f)
    return metrics["columnas_features"]

def predict(features: dict):
    model = load_model()
    scaler = load_scaler()
    columns = load_feature_columns()

    def normalize_key(col):
        return col.replace(" ", "_")

    X = np.array([[features.get(col, features.get(normalize_key(col), 0)) for col in columns]])
    X_scaled = scaler.transform(X)

    pred = model.predict(X_scaled)[0]
    proba = model.predict_proba(X_scaled)[0].tolist()
    return {
        "prediction": int(pred),
        "probability_no_default": round(proba[0], 4),
        "probability_default": round(proba[1], 4)
    }