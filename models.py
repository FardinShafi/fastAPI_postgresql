from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from database import Base

class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    department = Column(String)
    is_manager = Column(Boolean, default=False) 
    start_date = Column(Date)  

    department_id = Column(Integer, ForeignKey('department.id'))
    department = relationship("Department", back_populates="employees")

class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    grade = Column(Integer)
    is_active = Column(Boolean, default=True) 
    enrollment_date = Column(Date) 

    guardian_id = Column(Integer, ForeignKey('guardian.id'))
    guardian = relationship("Guardian", back_populates="students")

class Guardian(Base):
    __tablename__ = 'guardian'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contact_number = Column(String)

    students = relationship("Student", back_populates="guardian")

class Department(Base):
    __tablename__ = 'department'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    employees = relationship("Employee", back_populates="department")

class Tables(Base):
    __tablename__ = 'tables'

    id = Column(Integer, primary_key=True, index=True)
    table_name = Column(String, unique=True, index=True)

class Vendor(Base):
    __tablename__ = 'vendor'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contact_number = Column(String)
