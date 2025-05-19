# app.py
from flask import Flask, render_template, request, redirect, session, flash
from datetime import datetime
import db_utils
from salary_calculator import calculate_salary
from dateutil.parser import parse as date_parser

app = Flask(__name__)
app.secret_key = "your_secret_key"

# 📅 Custom filter for date formatting
def strftime_filter(value, format_string='%Y-%m-%d'):
    try:
        # If value is string, try parsing it into datetime object
        if isinstance(value, str):
            value = date_parser(value)

        # If it's a datetime object, format it
        if isinstance(value, datetime):
            return value.strftime(format_string)

        return value
    except Exception:
        return value

# 🔧 Register custom filter with Jinja2
app.jinja_env.filters['strftime'] = strftime_filter


# Admin credentials (for demo only)
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"


# 🔐 Admin Login Route
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == ADMIN_USER and password == ADMIN_PASS:
            session['admin'] = True
            return redirect('/admin/dashboard')
        else:
            flash("❌ Invalid credentials")
    return render_template('admin/login.html')


# 📊 Admin Dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect('/admin/login')

    employees = db_utils.list_all_employees()
    return render_template('admin/dashboard.html', employees=employees)


# 🔒 Admin Logout
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect('/')


# ➕ Add New Employee
@app.route('/admin/employee/add', methods=['GET', 'POST'])
def add_employee():
    if not session.get('admin'):
        return redirect('/admin/login')

    if request.method == 'POST':
        try:
            eid = int(request.form['employee_id'])
            fname = request.form['first_name']
            lname = request.form['last_name']
            gender = request.form['gender']
            sdate = request.form['start_date']
            years = int(request.form['years'])
            dept = request.form['department']
            country = request.form['country']
            msalary = float(request.form['monthly_salary'])
            asalary = float(request.form['annual_salary'])
            jrate = float(request.form['job_rate'])
            sick = int(request.form['sick_leave'])
            unpaids = int(request.form['unpaid_leaves'])
            ot = float(request.form['overtime_hours'])

            conn = db_utils.get_db_connection()
            cur = conn.cursor()
            cur.execute('''INSERT INTO employees VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
                          %s, %s, %s, %s, %s, %s)''',
                        (eid, fname, lname, gender, sdate, years, dept, country,
                         msalary, asalary, jrate, sick, unpaids, ot))
            conn.commit()
            conn.close()
            return redirect('/admin/dashboard')
        except Exception as e:
            flash(f"❌ Error adding employee: {e}")

    return render_template('admin/add_employee.html')


# 🗑️ Delete Employee
@app.route('/admin/employee/<int:eid>/delete')
def delete_employee(eid):
    if not session.get('admin'):
        return redirect('/admin/login')

    conn = db_utils.get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM employees WHERE employee_id = %s", (eid,))
    conn.commit()
    conn.close()
    return redirect('/admin/dashboard')


# 💼 Main Page - Employee Salary Lookup
@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    employee = None
    salary_details = {}

    if request.method == 'POST':
        try:
            eid = int(request.form['employee_id'])
            employee = db_utils.get_employee_by_id(eid)

            if not employee:
                error = "❌ Error: Your ID was not found."
            else:
                salary = calculate_salary(employee)
                salary_details.update({
                    'name': f"{employee['first_name']} {employee['last_name']}",
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    'employee_id': eid,
                    **salary
                })
        except ValueError:
            error = "❌ Error: Please enter a valid numeric Employee ID"

    return render_template('salary_invoice.html',
                           employee=employee,
                           salary=salary_details,
                           error=error)


# ✏️ Edit Employee
@app.route('/admin/employee/<int:eid>/edit', methods=['GET', 'POST'])
def edit_employee(eid):
    if not session.get('admin'):
        return redirect('/admin/login')

    conn = db_utils.get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM employees WHERE employee_id = %s", (eid,))
    row = cur.fetchone()
    columns = [desc[0] for desc in cur.description]
    employee = dict(zip(columns, row))
    conn.close()

    if not employee:
        flash("❌ Employee not found")
        return redirect('/admin/dashboard')

    if request.method == 'POST':
        try:
            fname = request.form['first_name']
            lname = request.form['last_name']
            gender = request.form['gender']
            sdate = request.form['start_date']
            years = int(request.form['years'])
            dept = request.form['department']
            country = request.form['country']
            msalary = float(request.form['monthly_salary'])
            asalary = float(request.form['annual_salary'])
            jrate = float(request.form['job_rate'])
            sick = int(request.form['sick_leave'])
            unpaids = int(request.form['unpaid_leaves'])
            ot = float(request.form['overtime_hours'])

            conn = db_utils.get_db_connection()
            cur = conn.cursor()
            cur.execute('''UPDATE employees SET first_name = %s, last_name = %s, gender = %s,
                          start_date = %s, years = %s, department = %s, country = %s,
                          monthly_salary = %s, annual_salary = %s, job_rate = %s,
                          sick_leave = %s, unpaid_leaves = %s, overtime_hours = %s
                          WHERE employee_id = %s''',
                        (fname, lname, gender, sdate, years, dept, country,
                         msalary, asalary, jrate, sick, unpaids, ot, eid))
            conn.commit()
            conn.close()
            return redirect('/admin/dashboard')
        except Exception as e:
            flash(f"❌ Error updating employee: {e}")

    return render_template('admin/edit_employee.html', employee=employee)


# Run App
if __name__ == '__main__':
    app.run(debug=True)