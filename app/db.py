import os
from dotenv import load_dotenv
try:
    import psycopg2
except ImportError:
    import psycopg as psycopg2

load_dotenv(override=True)

def get_connection():
    return psycopg2.connect(
        host=os.getenv("SUPABASE_DB_HOST"),
        port=int(os.getenv("SUPABASE_DB_PORT", "6543")),
        dbname=os.getenv("SUPABASE_DB_NAME", "postgres"),
        user=os.getenv("SUPABASE_DB_USER"),
        password=os.getenv("SUPABASE_DB_PASSWORD"),
        sslmode="require"
    )