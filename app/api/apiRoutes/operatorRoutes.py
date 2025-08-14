from fastapi import APIRouter, Depends, Header , HTTPException
from app.schemas.operatorSchema import OperatorCreate, OperatorUpdate, OperatorOut
from app.methods import operatorMethod

authController = APIRouter()
operatorController = APIRouter()

def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.split(" ")[1]
    return {"userId": 1, "email": "admin@admin.com", "role": "ADMIN"}


@operatorController.get("/", response_model=list[OperatorOut])
def list_operators(user=Depends(get_current_user)):
    return operatorMethod.get_operators()


@operatorController.post("/", response_model=OperatorOut)
def create_operator(payload: OperatorCreate, user=Depends(get_current_user)):
    return operatorMethod.create_operator(payload)


@operatorController.put("/{operator_id}", response_model=OperatorOut)
def update_operator(operator_id: int, payload: OperatorUpdate, user=Depends(get_current_user)):
    return operatorMethod.update_operator(operator_id, payload)
