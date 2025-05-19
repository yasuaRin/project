# import_data.py
import psycopg2
import csv
from datetime import datetime

conn = psycopg2.connect(
    dbname="payroll_db",
    user="postgres",
    password="admin",
    host="localhost",
    port=5432
)
cursor = conn.cursor()

# Drop table if exists
cursor.execute("DROP TABLE IF EXISTS employees CASCADE")

# Recreate table
cursor.execute('''CREATE TABLE employees (
                  employee_id INTEGER PRIMARY KEY,
                  first_name TEXT,
                  last_name TEXT,
                  gender TEXT,
                  start_date DATE,
                  years INTEGER,
                  department TEXT,
                  country TEXT,
                  monthly_salary NUMERIC(10,2),
                  annual_salary NUMERIC(10,2),
                  job_rate NUMERIC(5,2),
                  sick_leave INTEGER,
                  unpaid_leaves INTEGER,
                  overtime_hours NUMERIC(5,2))''')

with open('Copy of Employees(1).csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row

    for row in reader:
        try:
            emp_id = int(row[0])
            first_name = row[1]
            last_name = row[2]
            gender = row[3]

            # Parse date
            try:
                start_date = datetime.strptime(row[4], "%m/%d/%Y").date()
            except ValueError:
                start_date = None

            years = int(row[5]) if row[5].strip() else None
            department = row[6]
            country = row[7]
            monthly_salary = float(row[8]) if row[8].strip() else None
            annual_salary = float(row[9]) if row[9].strip() else None
            job_rate = float(row[10]) if row[10].strip() else None
            sick_leave = int(row[11]) if row[11].strip() else None
            unpaid_leaves = int(row[12]) if row[12].strip() else None
            overtime_hours = float(row[13]) if len(row) > 13 and row[13].strip() else None

            cursor.execute('''INSERT INTO employees VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                          (emp_id, first_name, last_name, gender, start_date,
                           years, department, country, monthly_salary,
                           annual_salary, job_rate, sick_leave,
                           unpaid_leaves, overtime_hours))
        except Exception as e:
            print(f"Error inserting row: {row} - {e}")

conn.commit()
conn.close()
print("✅ Data imported successfully.")