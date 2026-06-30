import os
from fastapi import FastAPI
from app.db import get_connection

app = FastAPI(title="MVP DataOps Loan")

@app.get("/")
def root():
    return {"message": "API MVP DataOps Loan activa"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/db-health")
def db_health():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        cur.close()
        conn.close()
        return {"status": "ok", "postgres_version": version}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    

@app.get("/loan-data")
def get_loan_data(limit: int = 10):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM loan_demo LIMIT %s;", (limit,))
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        cur.close()
        conn.close()
        return {"total": len(rows), "data": [dict(zip(columns, row)) for row in rows]}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.get("/loan-data/stats")
def get_loan_stats():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                COUNT(*) as total_registros,
                AVG(loan_amnt) as promedio_monto,
                MIN(loan_amnt) as minimo_monto,
                MAX(loan_amnt) as maximo_monto,
                SUM(CASE WHEN loan_status = 1 THEN 1 ELSE 0 END) as defaults,
                SUM(CASE WHEN loan_status = 0 THEN 1 ELSE 0 END) as no_defaults
            FROM loan_demo;
        """)
        row = cur.fetchone()
        columns = [desc[0] for desc in cur.description]
        cur.close()
        conn.close()
        return dict(zip(columns, row))
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    
from app.predict import predict as run_prediction
from pydantic import BaseModel

class LoanInput(BaseModel):
    person_gender_female: float = 1.0
    person_gender_male: float = 0.0
    person_education_Associate: float = 0.0
    person_education_Bachelor: float = 1.0
    person_education_Doctorate: float = 0.0
    person_education_High_School: float = 0.0
    person_education_Master: float = 0.0
    person_home_ownership_MORTGAGE: float = 0.0
    person_home_ownership_OTHER: float = 0.0
    person_home_ownership_OWN: float = 0.0
    person_home_ownership_RENT: float = 1.0
    loan_intent_DEBTCONSOLIDATION: float = 0.0
    loan_intent_EDUCATION: float = 1.0
    loan_intent_HOMEIMPROVEMENT: float = 0.0
    loan_intent_MEDICAL: float = 0.0
    loan_intent_PERSONAL: float = 0.0
    loan_intent_VENTURE: float = 0.0
    previous_loan_defaults_on_file_No: float = 1.0
    previous_loan_defaults_on_file_Yes: float = 0.0
    person_age: float = 24.0
    person_income: float = 50000.0
    person_emp_exp: float = 3.0
    loan_amnt: float = 10000.0
    loan_int_rate: float = 12.0
    loan_percent_income: float = 0.2
    cb_person_cred_hist_length: float = 3.0
    credit_score: float = 650.0

@app.post("/predict-loan")
def predict_loan(data: LoanInput):
    try:
        result = run_prediction(data.model_dump())
        return result
    except Exception as e:
        return {"status": "error", "detail": str(e)}