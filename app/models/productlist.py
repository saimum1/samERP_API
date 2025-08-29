# from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func
# # from sqlalchemy.ext.declarative import declarative_base
# from app.db.database import Base

# # Base = declarative_base()

# class Product(Base):
#     __tablename__ = "products"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255), nullable=False)
#     code = Column(String(50))
#     quantity = Column(Integer, default=0)
#     lot_no = Column(String(100))
#     logo = Column(String)
#     status = Column(String(200)) 
#     description = Column(Text)
#     category_id = Column(Integer, ForeignKey("operators.id"))
#     operator = relationship("Operator",lazy='noload')
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
# #     operator = relationship("Operator", back_populates="products")

# # from app.models.operators import Operator


# app/models/product.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    price: int = 0
    code: Optional[str] = None
    imageink1: Optional[str] = None
    imageink2: Optional[str] = None
    imageink3: Optional[str] = None
    imageink4: Optional[str] = None
    quantity: int = 0
    lot_no: Optional[str] = None
    logo: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    category_id : str
    operator_id: Optional[str] = None  # store Operator._id as string

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = 0
    imageink1: Optional[str] = None
    imageink2: Optional[str] = None
    imageink3: Optional[str] = None
    imageink4: Optional[str] = None
    code: Optional[str] = None
    quantity: Optional[int] = None
    lot_no: Optional[str] = None
    logo: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    operator_id: Optional[str] = None



class ProductOut(ProductBase):
    id: str = Field(..., alias="_id")
    category_id: str = Field(..., alias="categoryId")
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


