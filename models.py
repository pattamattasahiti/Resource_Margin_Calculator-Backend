from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    emp_code = Column(String(20), unique=True, nullable=False)
    name = Column(String(100))
    designation = Column(String(100))
    resource_type = Column(String(50))
    salary_p_a_inr = Column(Float)
    overhead_inr = Column(Float)
    conversion_rate = Column(Float)
    billing_rate_usd_hr = Column(Float)
    occupancy_rate = Column(Float)
    billable_per_hour_usd = Column(Float)
    overhead_usa_usd = Column(Float)
