from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models import Base
import enum

class DeviceStatus(str, enum.Enum):
    available = "available"
    pending_borrow = "pending_borrow"
    borrowed = "borrowed"
    pending_return = "pending_return"
    damaged = "damaged"
    repair_pending = "repair_pending"
    repairing = "repairing"
    repaired = "repaired"
    scrapped = "scrapped"
    offline = "offline"

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    image = Column(String(255), nullable=True)
    status = Column(SQLEnum(DeviceStatus), default=DeviceStatus.available)
    location = Column(String(100), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    creator = relationship("User", foreign_keys=[created_by], lazy="joined")