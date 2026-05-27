import pandas as pd
import psycopg
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

def get_connection_params():
    return {
        "host": os.getenv("SUPABASE_DB_HOST"),
        "port": os.getenv("SUPABASE_DB_PORT", "5432"),
        "dbname": os.getenv("SUPABASE_DB_NAME", "postgres"),
        "user": os.getenv("SUPABASE_DB_USER"),
        "password": os.getenv("SUPABASE_DB_PASSWORD"),
        "sslmode": "require",
    }

def cargar_csv():
    ruta = Path("data/02_loan_data.csv")
    
    if not ruta.exists():
        print(f"ERROR: No se encontró el archivo {ruta}")
        return

    df = pd.read_csv(ruta)
    print(f"Filas leidas desde CSV: {len(df)}")
    print(f"Columnas: {list(df.columns)}")

    # Limpiar valores nulos
    df = df.dropna(subset=["loan_status"])
    df["loan_status"] = df["loan_status"].astype(int)
    df["person_age"] = pd.to_numeric(df["person_age"], errors="coerce")
    df["person_income"] = pd.to_numeric(df["person_income"], errors="coerce")
    df["loan_amnt"] = pd.to_numeric(df["loan_amnt"], errors="coerce")
    df["loan_int_rate"] = pd.to_numeric(df["loan_int_rate"], errors="coerce")
    df["loan_percent_income"] = pd.to_numeric(df["loan_percent_income"], errors="coerce")
    df["cb_person_cred_hist_length"] = pd.to_numeric(df["cb_person_cred_hist_length"], errors="coerce")

    params = get_connection_params()

    with psycopg.connect(**params) as conn:
        with conn.cursor() as cur:
            # Limpiar tabla antes de cargar
            cur.execute("TRUNCATE TABLE public.loan_demo RESTART IDENTITY;")
            print("Tabla limpiada correctamente.")

            insert_query = """
                INSERT INTO public.loan_demo (
                    person_age, person_gender, person_education,
                    person_income, person_emp_exp, person_home_ownership,
                    loan_amnt, loan_intent, loan_int_rate,
                    loan_percent_income, cb_person_cred_hist_length,
                    credit_score, previous_loan_defaults_on_file, loan_status
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """

            registros = 0
            for _, row in df.iterrows():
                cur.execute(insert_query, (
                    row["person_age"],
                    row["person_gender"],
                    row["person_education"],
                    row["person_income"],
                    int(row["person_emp_exp"]),
                    row["person_home_ownership"],
                    row["loan_amnt"],
                    row["loan_intent"],
                    row["loan_int_rate"],
                    row["loan_percent_income"],
                    row["cb_person_cred_hist_length"],
                    int(row["credit_score"]),
                    row["previous_loan_defaults_on_file"],
                    int(row["loan_status"])
                ))
                registros += 1

        conn.commit()

    print(f"Carga completada correctamente en public.loan_demo")
    print(f"Total registros cargados: {registros}")

if __name__ == "__main__":
    cargar_csv()