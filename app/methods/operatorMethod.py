
# from sqlalchemy.orm import Session
# from sqlalchemy import select
# from sqlalchemy.exc import IntegrityError
# from fastapi import HTTPException, status
# from app.models.operators import Operator
# from app.schemas.operatorSchema import OperatorCreate, OperatorUpdate, OperatorOut

# def create_operator(db: Session, operator: OperatorCreate):
#     db_operator = Operator(**operator.model_dump())
#     try:
#         db.add(db_operator)
#         db.commit()
#         db.refresh(db_operator)
#         return OperatorOut.from_orm(db_operator)
#     except IntegrityError:
#         db.rollback()
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operator already exists")

# def update_operator(db: Session, operator_id: int, operator: OperatorUpdate):
#     db_operator = db.query(Operator).filter(Operator.id == operator_id).first()
#     if not db_operator:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operator not found")
    
#     update_data = operator.model_dump(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(db_operator, key, value)
    
#     try:
#         db.commit()
#         db.refresh(db_operator)
#         return OperatorOut.from_orm(db_operator)
#     except IntegrityError:
#         db.rollback()
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operator already exists")

# def get_operators(db: Session):
#     operators = db.query(Operator).all()
#     return operators

# def get_operator_by_id(db: Session, operator_id: int):
#     db_operator = db.query(Operator).filter(Operator.id == operator_id).first()
#     if not db_operator:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operator not found")
#     return OperatorOut.from_orm(db_operator)


# def delete_operator_by_id(db: Session, operator_id: int):
#     db_operator = db.query(Operator).filter(Operator.id == operator_id).first()
#     if not db_operator:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operator not found")
#     db.delete(db_operator)
#     db.commit()
#     return {"message": "Operator deleted successfully", "id": operator_id}


# app/crud/operator_crud.py
from fastapi import HTTPException, status
from app.models.operators import OperatorCreate, OperatorUpdate, OperatorOut
from bson import ObjectId
from datetime import datetime

async def create_operator(db, operator: OperatorCreate):
    existing = await db.operators.find_one({"name": operator.name})
    if existing:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operator already exists")

    doc = operator.model_dump()
    doc["created_at"] = datetime.utcnow()
    doc["updated_at"] = datetime.utcnow()

    result = await db.operators.insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    return OperatorOut(**doc)


async def update_operator(db, operator_id: str, operator: OperatorUpdate):
    update_data = {k: v for k, v in operator.model_dump(exclude_unset=True).items()}
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No data to update")
    update_data["updated_at"] = datetime.utcnow()

    result = await db.operators.update_one(
        {"_id": ObjectId(operator_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operator not found")

    updated = await db.operators.find_one({"_id": ObjectId(operator_id)})
    updated["_id"] = str(updated["_id"])
    return OperatorOut(**updated)


async def get_operators(db):
    cursor = db.operators.find()
    operators = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        operators.append(OperatorOut(**doc))
    return operators


async def get_operator_by_id(db, operator_id: str):
    doc = await db.operators.find_one({"_id": ObjectId(operator_id)})
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operator not found")
    doc["_id"] = str(doc["_id"])
    return OperatorOut(**doc)


async def delete_operator_by_id(db, operator_id: str):
    result = await db.operators.delete_one({"_id": ObjectId(operator_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operator not found")
    return {"message": "Operator deleted successfully", "id": operator_id}
