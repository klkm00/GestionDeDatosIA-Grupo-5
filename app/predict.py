import joblib
import numpy as np
import os

MODEL_PATH = os.path.join("artifacts", "loan_model.joblib")

def load_model():
    return joblib.load(MODEL_PATH)

def predict(features: dict):
    model = load_model()
    columns = model.feature_names_in_
    X = np.array([[features.get(col, 0) for col in columns]])
    pred = model.predict(X)[0]
    proba = model.predict_proba(X)[0].tolist()
    return {
        "prediction": int(pred),
        "probability_no_default": round(proba[0], 4),
        "probability_default": round(proba[1], 4)
    }