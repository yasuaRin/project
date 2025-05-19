# salary_calculator.py
from decimal import Decimal
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# Set up Jinja2 environment once
env = Environment(loader=FileSystemLoader('templates'))
from decimal import Decimal, ROUND_HALF_UP

def calculate_salary(employee):
    USD_TO_IDR = Decimal('15000')
    
    base_salary_usd = Decimal(employee['monthly_salary'])
    hourly_rate_usd = (base_salary_usd / Decimal('22')) / Decimal('8')

    ot_pay_usd = hourly_rate_usd * Decimal(employee['overtime_hours'])
    deduction_usd = (base_salary_usd / Decimal('22')) * Decimal(employee['unpaid_leaves'])

    # Convert to IDR and round properly
    base_salary_idr = int((base_salary_usd * USD_TO_IDR).quantize(Decimal('1000'), rounding=ROUND_HALF_UP))
    ot_pay_idr = int((ot_pay_usd * USD_TO_IDR).quantize(Decimal('1000'), rounding=ROUND_HALF_UP))
    deduction_idr = int((deduction_usd * USD_TO_IDR).quantize(Decimal('1000'), rounding=ROUND_HALF_UP))

    gross_monthly_idr = base_salary_idr + ot_pay_idr
    tax_rate = Decimal('0.06') if gross_monthly_idr > 6_000_000 else Decimal('0.03')
    tax_amount_idr = int((gross_monthly_idr * tax_rate).quantize(Decimal('1000'), rounding=ROUND_HALF_UP))

    net_monthly_idr = gross_monthly_idr - deduction_idr - tax_amount_idr
    net_annual_idr = net_monthly_idr * 12

    # Add gross_annual
    gross_annual_idr = gross_monthly_idr * 12

    return {
        'base_salary': base_salary_idr,
        'ot_hours': employee['overtime_hours'],
        'hourly_rate': int((hourly_rate_usd * USD_TO_IDR).quantize(Decimal('1000'), rounding=ROUND_HALF_UP)),
        'ot_pay': ot_pay_idr,
        'deduction': deduction_idr,
        'gross_monthly': gross_monthly_idr,
        'gross_annual': gross_annual_idr,  # ✅ Added this line
        'tax_rate': float(tax_rate * 100),
        'tax_amount': tax_amount_idr,
        'net_monthly': int(Decimal(net_monthly_idr).quantize(Decimal('1000'), rounding=ROUND_HALF_UP)),
        'net_annual': int(Decimal(net_annual_idr).quantize(Decimal('1000'), rounding=ROUND_HALF_UP)),
    }
def generate_salary_invoice(employee_id):
    from db_utils import get_employee_by_id

    employee = get_employee_by_id(employee_id)
    if not employee:
        return "Employee not found"

    salary_details = calculate_salary(employee)
    name = f"{employee['first_name']} {employee['last_name']}"

    salary_details.update({
        'name': name,
        'date': datetime.now().strftime("%Y-%m-%d"),
        'employee_id': employee_id
    })

    template = env.get_template('salary_invoice.html')
    html_content = template.render(salary=salary_details, employee=employee)

    filename = f"invoice_{employee_id}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return f"Invoice saved as {filename}"