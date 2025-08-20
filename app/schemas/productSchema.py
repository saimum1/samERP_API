from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.operatorSchema import OperatorOut,OperatorBase
class ProductBase(BaseModel):
    name: str
    code: str
    quantity: int = 0
    lot_no: str = Field(None, alias="lotNo")
    logo: str = None
    status: str
    description: str = None
    category_id: int = Field(None, alias="categoryId")
    # created_at: str = None
    # updated_at: str = None
    model_config = {
    "from_attributes": True,
    "populate_by_name": True 
    }

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: str
    operator: OperatorOut | None = None
    class Config:
        from_attributes = True
    
 