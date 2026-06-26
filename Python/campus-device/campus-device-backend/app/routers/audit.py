from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import get_db
from app.dependencies import get_current_user, require_role
from app.repositories.audit_repo import AuditRepository
from app.utils.response_util import Result

router = APIRouter()

@router.get("/audit-logs")
async def get_audit_logs(
    target_type: str,
    target_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    repo = AuditRepository(db)
    data = await repo.get_by_target(target_type, target_id, page=page, page_size=page_size)
    return Result.success(data=data)