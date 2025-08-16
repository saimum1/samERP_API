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
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True