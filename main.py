from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from database import Base, SessionLocal, engine
import models
from typing import Type

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Create tables in the database
models.Base.metadata.create_all(bind=engine)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to get table names
@app.get("/tables", response_model=list)
def get_tables():
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    return table_names

# Endpoint to get column names and data types for a specific table
# @app.get("/tables/{table_name}/columns", response_model=dict)
# def get_columns(table_name: str, db: Session = Depends(get_db)):
#     if table_name == "employee":
#         table = models.Employee
#     elif table_name == "student":
#         table = models.Student
#     elif table_name == "guardian":
#         table = models.Guardian
#     else:
#         raise HTTPException(status_code=404, detail="Table not found")
    
#     columns = {}
#     for column in table.__table__.columns:
#         columns[column.name] = str(column.type)
    
#     return columns

@app.get("/tables/{table_name}/columns", response_model=dict)
def get_columns(table_name: str, db: Session = Depends(get_db)) -> dict:
    
    model_class = getattr(models, table_name.capitalize(), None)

    if model_class is None:
        raise HTTPException(status_code=404, detail="Table not found")
    
    # Get the column names and data types for the table
    columns = {}
    for column in model_class.__table__.columns:
        columns[column.name] = str(column.type)
    
    return columns