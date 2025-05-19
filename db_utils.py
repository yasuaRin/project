# db_utils.py
import psycopg2

def get_db_connection():
    return psycopg2.connect(
        dbname="payroll_db",
        user="postgres",
        password="admin",
        host="localhost",
        port="5432"
    )

def get_employee_by_id(employee_id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM employees WHERE employee_id = %s", (employee_id,))
                row = cur.fetchone()
                if not row:
                    return None
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, row))
    except Exception as e:
        print(f"[ERROR] Database error: {e}")
        return None

def list_all_employees():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM employees ORDER BY employee_id ASC")
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in rows]