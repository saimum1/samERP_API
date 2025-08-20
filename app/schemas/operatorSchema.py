from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OperatorBase(BaseModel):
    name: str
    code: str
    logo: Optional[str] = None
    status: str

class OperatorCreate(OperatorBase):
    pass

class OperatorUpdate(OperatorBase):
    pass

class OperatorOut(OperatorBase):
    id: str 
    model_config = {    
    "from_attributes": True,
    "populate_by_name": True  
    }