from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BorrowCreateRequest(BaseModel):
    device_id: int
    borrow_reason: Optional[str] = None
    expected_return_time: Optional[str] = None  # ISO 8601 格式


class BorrowAuditRequest(BaseModel):
    action: str  # "approve" 或 "reject"
    remark: Optional[str] = None


class BorrowReturnRequest(BaseModel):
    return_status: str  # "normal" 或 "damaged"
    damage_description: Optional[str] = None


class BorrowResponse(BaseModel):
    id: int
    device_id: int
    user_id: int
    status: str
    borrow_reason: Optional[str] = None
    borrow_time: Optional[datetime] = None
    expected_return_time: Optional[datetime] = None
    actual_return_time: Optional[datetime] = None
    return_status: Optional[str] = None
    damage_description: Optional[str] = None
    audit_by: Optional[int] = None
    audit_time: Optional[datetime] = None
    audit_remark: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    # 关联信息
    device_name: Optional[str] = None
    user_name: Optional[str] = None

    model_config = {"from_attributes": True}