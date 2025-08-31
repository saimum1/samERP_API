from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import uuid4,UUID
from typing import List
from app.models.productlist import ProductResponse
from app.models.operators import OperatorResponse

class Item(BaseModel):
    productid: Optional[str] = None
    name: Optional[str] = None
    price: Optional[int] = 0
    image: Optional[str] = None
    quantity: Optional[int] = 0
    leadname: Optional[str] = None
    leademail: Optional[str] = None
    product: Optional[ProductResponse] = None
    operator: Optional[OperatorResponse] = None




class OrderCreate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))  
    leadname: Optional[str] = None
    leademail: Optional[str] = None
    orderid:UUID= str(uuid4())
    status: str ='pending'
    items: List[Item] 


class OrderResponse(BaseModel):
    id: str
    orderid:str
    items: List[Item]
    created_at: datetime
    updated_at: datetime
    mongo_id: str = Field(..., alias="_id")
    created_at: datetime
    updated_at: datetime
    leadname: Optional[str] = None
    leademail: Optional[str] = None
    status: str