from pydantic import BaseModel

class OperatorBase(BaseModel):
    name: str
    code: str
    logo: str | None = None
    status: str = "not_available"

class OperatorCreate(OperatorBase):
    pass

class OperatorUpdate(OperatorBase):
    pass

class OperatorOut(OperatorBase):
    id: int

    class Config:
        orm_mode = True
