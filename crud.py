from sqlalchemy.orm import Session
from models import Employee

def create_employee(db: Session, emp_data: dict):
    db_emp = Employee(**emp_data)
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp

def get_employee_by_code(db: Session, emp_code: str):
    return db.query(Employee).filter(Employee.emp_code == emp_code).first()

def get_all_employees(db: Session):
    return db.query(Employee).all()

def update_employee(db: Session, emp_code: str, updates: dict):
    db_emp = get_employee_by_code(db, emp_code)
    if db_emp:
        for key, value in updates.items():
            setattr(db_emp, key, value)
        db.commit()
        db.refresh(db_emp)
    return db_emp

def delete_employee(db: Session, emp_code: str):
    db_emp = get_employee_by_code(db, emp_code)
    if db_emp:
        db.delete(db_emp)
        db.commit()
    return db_emp
