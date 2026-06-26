from dataclasses import dataclass
from fastapi import Depends, HTTPException, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.config import settings
from app.utils.jwt_util import verify_token

security = HTTPBearer()


@dataclass
class TokenPayload:
    """JWT Token 解析后的用户信息"""
    id: int
    role: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("user_id"),
            role=data.get("role", ""),
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> TokenPayload:
    """从 Authorization Header 提取 token，验证并返回用户信息"""
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="无效的认证令牌")
    return TokenPayload.from_dict(payload)


def require_role(*roles: str):
    """返回角色校验依赖，检查用户角色是否在允许列表中"""

    async def role_checker(
        current_user: TokenPayload = Depends(get_current_user),
    ):
        if current_user.role not in roles:
            raise HTTPException(status_code=403, detail="权限不足")
        return current_user

    return role_checker


async def get_pagination(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
):
    """分页参数依赖，page_size 最大 100"""
    return {"page": page, "page_size": page_size}