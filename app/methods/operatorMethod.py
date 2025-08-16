# methods/operatorMethod.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models.operators import Operator
from app.schemas.operatorSchema import OperatorCreate, OperatorUpdate, OperatorOut

def create_operator(db: Session, operator: OperatorCreate):
    db_operator = Operator(**operator.model_dump())
    try:
        db.add(db_operator)
        db.commit()
        db.refresh(db_operator)
        return OperatorOut.from_orm(db_operator)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operator already exists")

def update_operator(db: Session, operator_id: int, operator: OperatorUpdate):
    db_operator = db.query(Operator).filter(Operator.id == operator_id).first()
    if not db_operator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operator not found")
    
    update_data = operator.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_operator, key, value)
    
    try:
        db.commit()
        db.refresh(db_operator)
        return OperatorOut.from_orm(db_operator)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operator already exists")

def get_operators(db: Session):
    operators = db.query(Operator).all()
    return [OperatorOut.from_orm(op) for op in operators]

def get_operator_by_id(db: Session, operator_id: int):
    db_operator = db.query(Operator).filter(Operator.id == operator_id).first()
    if not db_operator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operator not found")
    return OperatorOut.from_orm(db_operator)


def delete_operator_by_id(db: Session, operator_id: int):
    db_operator = db.query(Operator).filter(Operator.id == operator_id).first()
    if not db_operator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operator not found")
    db.delete(db_operator)
    db.commit()
    return {"message": "Operator deleted successfully", "id": operator_id}