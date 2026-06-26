from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.models import get_db
from app.dependencies import get_current_user, require_role
from app.repositories.user_repo import UserRepository
from app.utils.response_util import Result

router = APIRouter()


@router.get("")
async def get_users(
    role: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    """获取用户列表，支持按角色筛选"""
    repo = UserRepository(db)
    if role:
        data = await repo.get_by_role(role=role, page=page, page_size=page_size)
    else:
        # 暂不支持获取全部用户，必须指定角色
        data = {"list": [], "total": 0, "page": page, "page_size": page_size, "total_pages": 0}
    return Result.success(data=data)