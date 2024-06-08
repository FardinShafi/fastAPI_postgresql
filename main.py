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
def get_tables(db: Session = Depends(get_db)):
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    
    # Sort the table names in alphanumeric order
    table_names.sort()
    
    # Update the tables table in the database
    Tables = models.Tables
    existing_tables = [table.table_name for table in db.query(Tables).all()]
    
    for table_name in table_names:
        if table_name not in existing_tables:
            db_table = Tables(table_name=table_name)
            db.add(db_table)
    
    db.commit()
    
    return table_names

# Endpoint to get column names and data types for a specific table
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

# Endpoint to get the list of tables from the tables table
@app.get("/all-tables", response_model=list)
def get_all_tables(db: Session = Depends(get_db)):
    Tables = models.Tables
    tables = db.query(Tables).all()
    table_names = sorted([table.table_name for table in tables])
    
    return table_names
