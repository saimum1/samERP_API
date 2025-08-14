from fastapi import HTTPException
from app.schemas.operatorSchema import OperatorCreate, OperatorUpdate
from datetime import datetime


OPERATORS_DB = []
NEXT_ID = 1

def get_operators():
    return OPERATORS_DB

def create_operator(payload: OperatorCreate):
    global NEXT_ID
    if any(op['code'] == payload.code for op in OPERATORS_DB):
        raise HTTPException(status_code=403, detail="Operator already exists")
    print("data----",payload)
    operator = payload.dict()
    operator['id'] = NEXT_ID
    NEXT_ID += 1
    OPERATORS_DB.append(operator)
    return operator

def update_operator(operator_id: int, payload: OperatorUpdate):
    operator = next((op for op in OPERATORS_DB if op['id'] == operator_id), None)
    if not operator:
        raise HTTPException(status_code=404, detail="Operator not found")

    if any(op['code'] == payload.code and op['id'] != operator_id for op in OPERATORS_DB):
        raise HTTPException(status_code=403, detail="Operator code already exists")

    operator.update(payload.dict())
    return operator
