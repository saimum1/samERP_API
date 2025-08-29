# from pydantic import BaseModel, Field
# from typing import Optional
# from app.schemas.operatorSchema import OperatorOut,OperatorBase
# class ProductBase(BaseModel):
#     name: str
#     price: int = 0
#     imageink1: Optional[str] = ""
#     imageink2: Optional[str] = ""
#     imageink3: Optional[str] = ""
#     imageink4: Optional[str] = ""
#     code: str | int
#     quantity: int = 0
#     lot_no: str = Field(None, alias="lotNo")
#     logo: str = None
#     status: str
#     description: str = None
#     category_id: str  = Field(None, alias="categoryId")
#     # created_at: str = None
#     # updated_at: str = None
#     model_config = {
#     "from_attributes": True,
#     "populate_by_name": True 
#     }

# class ProductCreate(ProductBase):
#     pass

# class ProductUpdate(ProductBase):
#     pass

# class ProductOut(ProductBase):
#     id: str = Field(..., alias="id")
#     operator: OperatorOut | None = None
#     class Config:
#         from_attributes = True
    
 

# class ProductResponse(ProductBase):
#     products: list[ProductOut]
#     totalPages: int
#     totalCount: int 




from pydantic import BaseModel, Field
from typing import Optional, List
from app.schemas.operatorSchema import OperatorOut

class ProductBase(BaseModel):
    name: str
    price: int = 0
    imageink1: Optional[str] = ""
    imageink2: Optional[str] = ""
    imageink3: Optional[str] = ""
    imageink4: Optional[str] = ""
    code: str | int
    quantity: int = 0
    lot_no: str = Field(None, alias="lotNo")
    logo: Optional[str] = None
    status: str
    description: Optional[str] = None
    category_id: Optional[str] = Field(None, alias="categoryId")
    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: str = Field(..., alias="id")
    operator: Optional[OperatorOut] = None
    class Config:
        from_attributes = True

class ProductResponse(BaseModel):  # Remove inheritance from ProductBase
    products: List[ProductOut]
    totalPages: int
    totalCount: int
    model_config = {
        "from_attributes": True 
    }