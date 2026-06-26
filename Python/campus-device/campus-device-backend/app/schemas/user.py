from pydantic import BaseModel
from typing import Optional


class UserRegisterRequest(BaseModel):
    username: str
    phone: str
    password: str
    role: str = "student"


class UserLoginRequest(BaseModel):
    phone: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    phone: str
    email: Optional[str] = None
    role: str
    avatar: Optional[str] = None
    is_active: bool
    created_at: Optional[str] = None

    model_config = {"from_attributes": True}