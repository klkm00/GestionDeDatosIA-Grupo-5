import os
import json
import joblib
import numpy as np
from dotenv import load_dotenv
from app.db import get_connection
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

load_dotenv(override=True)

TARGET = os.getenv("MODEL_TARGET_COLUMN", "loan_status")

print("Conectando a Supabase...")
conn = get_connection()
cur = conn.cursor()
cur.execute("SELECT * FROM loan_demo;")
rows = cur.fetchall()
columns = [desc[0] for desc in cur.description]
cur.close()
conn.close()

import pandas as pd
df = pd.DataFrame(rows, columns=columns)
print(f"Datos cargados: {df.shape}")

# Separar features y target
drop_cols = [TARGET, "fecha_procesamiento", "categoria_credito"]
X = df.drop(columns=[c for c in drop_cols if c in df.columns])
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Entrenando modelo...")
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, output_dict=True)
cm = confusion_matrix(y_test, y_pred).tolist()

metrics = {
    "accuracy": acc,
    "classification_report": report,
    "confusion_matrix": cm
}

os.makedirs("artifacts", exist_ok=True)
joblib.dump(model, "artifacts/loan_model.joblib")
with open("artifacts/loan_metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)

print(f"Accuracy: {acc:.4f}")
print("Modelo guardado en artifacts/loan_model.joblib")
print("Métricas guardadas en artifacts/loan_metrics.json")