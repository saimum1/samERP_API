# from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, func
# from app.db.database import Base
# import enum
# from sqlalchemy.orm import relationship


# class OperatorStatus(str, enum.Enum):
#     available = "available"
#     not_available = "not_available"

# class Operator(Base):
#     __tablename__ = "operators"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255), unique=True, nullable=False)
#     code = Column(String(20), nullable=False)
#     logo = Column(Text)
#     status = Column(Enum(OperatorStatus), nullable=False)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
#     products = relationship("Product", lazy='noload')


from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime


class OperatorStatus(str, Enum):
    available = "available"
    not_available = "not_available"


class OperatorBase(BaseModel):
    name: str
    code: str
    logo: Optional[str] = None
    status: OperatorStatus


class OperatorCreate(OperatorBase):
    pass


class OperatorUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    logo: Optional[str] = None
    status: Optional[OperatorStatus] = None


class OperatorOut(OperatorBase):
    id: str = Field(..., alias="_id") 
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True 
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
   