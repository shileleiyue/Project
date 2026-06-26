from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DeviceCreateRequest(BaseModel):
    name: str
    type: str
    description: Optional[str] = None
    location: Optional[str] = None
    image: Optional[str] = None

class DeviceUpdateRequest(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    image: Optional[str] = None

class DeviceResponse(BaseModel):
    id: int
    name: str
    type: str
    description: Optional[str] = None
    image: Optional[str] = None
    status: str
    location: Optional[str] = None
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}