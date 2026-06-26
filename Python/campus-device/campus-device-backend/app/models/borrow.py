from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models import Base
import enum

class BorrowStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    borrowing = "borrowing"
    pending_return = "pending_return"
    returned = "returned"
    damaged_returned = "damaged_returned"

class ReturnStatus(str, enum.Enum):
    normal = "normal"
    damaged = "damaged"

class Borrow(Base):
    __tablename__ = "borrows"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(SQLEnum(BorrowStatus), nullable=False, default=BorrowStatus.pending)
    borrow_reason = Column(String(255), nullable=True)
    borrow_time = Column(DateTime, nullable=True)
    expected_return_time = Column(DateTime, nullable=True)
    actual_return_time = Column(DateTime, nullable=True)
    return_status = Column(SQLEnum(ReturnStatus), nullable=True)
    damage_description = Column(Text, nullable=True)
    audit_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    audit_time = Column(DateTime, nullable=True)
    audit_remark = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    device = relationship("Device")
    user = relationship("User", foreign_keys=[user_id])
    auditor = relationship("User", foreign_keys=[audit_by])