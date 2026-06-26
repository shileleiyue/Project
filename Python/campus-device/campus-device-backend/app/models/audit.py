from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    target_type = Column(String(50), nullable=False)
    target_id = Column(Integer, nullable=False)
    action = Column(String(50), nullable=False)
    from_status = Column(String(50), nullable=True)
    to_status = Column(String(50), nullable=True)
    operator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    remark = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    operator = relationship("User", foreign_keys=[operator_id])