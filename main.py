from fastapi import FastAPI, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session

from db import SessionLocal
from models import Base, Employee
from crud import (
    create_employee,
    get_employee_by_code,
    get_all_employees,
    update_employee,
    delete_employee
)
from logic import (
    calculate_bonus,
    calculate_india_margin,
    calculate_salary_p_a_usd,
    calculate_salary_p_m_usd,
    calculate_billable_p_a_usd,
    calculate_overhead_bonus_margin_usd,
    calculate_ctc_p_a_usa,
    calculate_ctc_p_m_usa,
    calculate_margin_p_a_usd,
    calculate_margin_on_sales,
    calculate_cost_per_hour
)
from excel_utils import make_excel
from db import engine
from models import Base

# Create DB tables (run at startup)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add this immediately after "app = FastAPI()"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # WARNING: open for any origin, use only for testing!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class EmployeeInput(BaseModel):
    emp_code: str
    name: str
    designation: str
    resource_type: str
    salary_p_a_inr: Optional[float] = 0
    overhead_inr: Optional[float] = 0
    conversion_rate: Optional[float] = 0
    billing_rate_usd_hr: Optional[float] = 0
    occupancy_rate: Optional[float] = 0
    billable_per_hour_usd: Optional[float] = 0
    overhead_usa_usd: Optional[float] = 0

def process_employee(employee: EmployeeInput):
    bonus_inr = calculate_bonus(employee.salary_p_a_inr)
    india_margin_inr = calculate_india_margin(employee.salary_p_a_inr, bonus_inr, employee.overhead_inr)
    salary_p_a_usd = calculate_salary_p_a_usd(employee.salary_p_a_inr, employee.conversion_rate)
    salary_p_m_usd = calculate_salary_p_m_usd(salary_p_a_usd)
    billable_p_a_usd = calculate_billable_p_a_usd(employee.billable_per_hour_usd, employee.occupancy_rate)
    overhead_bonus_margin_usd = calculate_overhead_bonus_margin_usd(
        employee.overhead_inr, bonus_inr, india_margin_inr, employee.conversion_rate
    )
    ctc_p_a_usa = calculate_ctc_p_a_usa(salary_p_a_usd, overhead_bonus_margin_usd, employee.overhead_usa_usd)
    ctc_p_m_usa = calculate_ctc_p_m_usa(ctc_p_a_usa)
    margin_p_a_usd = calculate_margin_p_a_usd(billable_p_a_usd, ctc_p_a_usa)
    margin_on_sales = calculate_margin_on_sales(margin_p_a_usd, billable_p_a_usd)
    cost_per_hour = calculate_cost_per_hour(employee.occupancy_rate)

    return {
        "EMP CODE": employee.emp_code,
        "NAME": employee.name,
        "DESIGNATION": employee.designation,
        "RESOURCE TYPE": employee.resource_type,
        "SALARY P.A (INR)": employee.salary_p_a_inr,
        "Bonus P.A (INR)": bonus_inr,
        "OverHead (INR)": employee.overhead_inr,
        "India Margin (INR)": india_margin_inr,
        "Salary P.A (USD)": salary_p_a_usd,
        "Salary P.M (USD)": salary_p_m_usd,
        "Billing Rate (USD/hr)": employee.billing_rate_usd_hr,
        "Occupancy Rate": employee.occupancy_rate,
        "Billable P.A (USD)": billable_p_a_usd,
        "Overhead+Bonus+India Margin (USD)": overhead_bonus_margin_usd,
        "Overhead USA (USD)": employee.overhead_usa_usd,
        "CTC P.A USA": ctc_p_a_usa,
        "CTC P.M USA": ctc_p_m_usa,
        "Margin P.A USD": margin_p_a_usd,
        "Margin on Sales %": margin_on_sales,
        "Cost per hour": cost_per_hour,
    }

@app.get("/")
def read_root():
    return {"message": "Your backend is running!"}

@app.post("/calculate")
def calculate_employee(employee: EmployeeInput):
    return process_employee(employee)

@app.post("/calculate/batch")
def calculate_batch(employees: List[EmployeeInput]):
    return [process_employee(emp) for emp in employees]

@app.post("/download_excel")
def download_excel(employees: List[EmployeeInput]):
    results = [process_employee(emp) for emp in employees]
    excel_path = make_excel(results)
    with open(excel_path, "rb") as f:
        content = f.read()
    return Response(
        content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=resource_margin_calc.xlsx"}
    )

# CRUD Endpoints (sample for create & view all)
@app.post("/employee/create")
def create_employee_endpoint(employee: EmployeeInput, db: Session = Depends(get_db)):
    emp_dict = employee.dict()
    db_emp = create_employee(db, emp_dict)
    return db_emp

@app.get("/employee/all")
def get_all_employees_endpoint(db: Session = Depends(get_db)):
    return get_all_employees(db)

@app.get("/employee/{emp_code}")
def get_employee_by_code_endpoint(emp_code: str, db: Session = Depends(get_db)):
    db_emp = get_employee_by_code(db, emp_code)
    if db_emp:
        return db_emp
    raise HTTPException(status_code=404, detail="Employee not found")

@app.put("/employee/{emp_code}")
def update_employee_endpoint(emp_code: str, updates: dict, db: Session = Depends(get_db)):
    db_emp = update_employee(db, emp_code, updates)
    if db_emp:
        return db_emp
    raise HTTPException(status_code=404, detail="Employee not found")

@app.delete("/employee/{emp_code}")
def delete_employee_endpoint(emp_code: str, db: Session = Depends(get_db)):
    db_emp = delete_employee(db, emp_code)
    if db_emp:
        return {"detail": f"Employee {emp_code} deleted"}
    raise HTTPException(status_code=404, detail="Employee not found")
