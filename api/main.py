from fastapi import FastAPI, Response, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Employee  # adjust as needed
from crud import (
    create_employee, get_employee_by_code, get_all_employees,
    update_employee, delete_employee
)

app = FastAPI()

# CORS (adjust origins for security in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

@app.get("/")
def root():
    return {"message": "Backend is running!"}

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
c