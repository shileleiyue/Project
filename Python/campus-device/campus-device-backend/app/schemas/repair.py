from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class RepairCreateRequest(BaseModel):
    device_id: int
    fault_description: Optional[str] = None
    borrow_id: Optional[int] = None


class RepairAssignRequest(BaseModel):
    assigned_to: int


class RepairStatusUpdateRequest(BaseModel):
    status: str  # repairing/repaired/unfixable
    repair_process: Optional[str] = None
    repair_result: Optional[str] = None


class RepairImageResponse(BaseModel):
    id: int
    repair_id: int
    image_type: str
    image_path: str
    uploaded_by: int
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class RepairResponse(BaseModel):
    id: int
    device_id: int
    borrow_id: Optional[int] = None
    reporter_id: int
    assigned_to: Optional[int] = None
    status: str
    fault_description: Optional[str] = None
    repair_process: Optional[str] = None
    repair_result: Optional[str] = None
    is_confirmed: bool = False
    confirmed_by: Optional[int] = None
    confirmed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    # 关联
    device_name: Optional[str] = None
    reporter_name: Optional[str] = None
    assignee_name: Optional[str] = None
    images: Optional[List[RepairImageResponse]] = None

    model_config = {"from_attributes": True}