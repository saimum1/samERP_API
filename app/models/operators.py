from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, func
from app.db.database import Base
import enum

class OperatorStatus(str, enum.Enum):
    available = "available"
    not_available = "not_available"

class Operator(Base):
    __tablename__ = "operators"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    code = Column(String(20), nullable=False)
    logo = Column(Text)
    status = Column(Enum(OperatorStatus), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())