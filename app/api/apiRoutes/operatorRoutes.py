# app/api/operatorRoutes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import operatorSchema 
from app.methods import operatorMethod

operatorController = APIRouter()

@operatorController.post("/", response_model=operatorSchema.OperatorOut)
def create_operator(operator: operatorSchema.OperatorCreate, db: Session = Depends(get_db)):
    if operator.status not in ["available", "not_available"]:
        raise HTTPException(status_code=422, detail="Status must be 'available' or 'not_available'")
    return operatorMethod.create_operator(db, operator)

@operatorController.get("/", response_model=list[operatorSchema.OperatorOut])
def list_operators(db: Session = Depends(get_db)):
    data=operatorMethod.get_operators(db)
    return operatorMethod.get_operators(db)

@operatorController.get("/{operator_id}", response_model=operatorSchema.OperatorOut)
def get_operator(operator_id: int, db: Session = Depends(get_db)):
    db_operator = operatorMethod.get_operator_by_id(db, operator_id)
    if not db_operator:
        raise HTTPException(status_code=404, detail="Operator not found")
    return db_operator

@operatorController.put("/{operator_id}", response_model=operatorSchema.OperatorOut)
def update_operator(operator_id: int, operator: operatorSchema.OperatorUpdate, db: Session = Depends(get_db)):
    if operator.status and operator.status not in ["available", "not_available"]:
        raise HTTPException(status_code=422, detail="Status must be 'available' or 'not_available'")
    db_operator = operatorMethod.update_operator(db, operator_id, operator)
    if not db_operator:
        raise HTTPException(status_code=404, detail="Operator not found")
    return db_operator



@operatorController.delete("/{operator_id}")
def delete_operator(operator_id: int, db: Session = Depends(get_db)):
    db_operator = operatorMethod.delete_operator_by_id(db, operator_id)
    return db_operator 