from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models import Base
import enum

class RepairStatus(str, enum.Enum):
    pending = "pending"
    assigned = "assigned"
    repairing = "repairing"
    repaired = "repaired"
    unfixable = "unfixable"
    completed = "completed"

class RepairImageType(str, enum.Enum):
    damage = "damage"
    before_repair = "before_repair"
    after_repair = "after_repair"

class Repair(Base):
    __tablename__ = "repairs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    borrow_id = Column(Integer, ForeignKey("borrows.id"), nullable=True)
    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(SQLEnum(RepairStatus), default=RepairStatus.pending)
    fault_description = Column(Text, nullable=True)
    repair_process = Column(Text, nullable=True)
    repair_result = Column(Text, nullable=True)
    is_confirmed = Column(Boolean, default=False)
    confirmed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    confirmed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    device = relationship("Device", lazy="joined")
    reporter = relationship("User", foreign_keys=[reporter_id], lazy="joined")
    assignee = relationship("User", foreign_keys=[assigned_to], lazy="joined")
    confirmer = relationship("User", foreign_keys=[confirmed_by], lazy="joined")
    images = relationship("RepairImage", back_populates="repair", lazy="selectin")


class RepairImage(Base):
    __tablename__ = "repair_images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    repair_id = Column(Integer, ForeignKey("repairs.id"), nullable=False)
    image_type = Column(SQLEnum(RepairImageType), nullable=False)
    image_path = Column(String(255), nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    repair = relationship("Repair", back_populates="images")
    uploader = relationship("User", foreign_keys=[uploaded_by], lazy="joined")