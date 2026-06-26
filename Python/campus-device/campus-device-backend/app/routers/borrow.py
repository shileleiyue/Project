from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.models import get_db
from app.dependencies import get_current_user, require_role
from app.schemas.borrow import (
    BorrowCreateRequest,
    BorrowAuditRequest,
    BorrowReturnRequest,
)
from app.services.borrow_service import BorrowService
from app.utils.response_util import Result

router = APIRouter()


@router.post("")
async def create_borrow(
    req: BorrowCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role("student")),
):
    service = BorrowService(db)
    borrow = await service.create_borrow(req, current_user.id)
    return Result.success(data=borrow, msg="借用申请已提交")


@router.get("")
async def get_borrows(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    service = BorrowService(db)
    data = await service.get_borrows(page=page, page_size=page_size, status=status)
    return Result.success(data=data)


@router.get("/my")
async def get_my_borrows(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = BorrowService(db)
    data = await service.get_my_borrows(
        current_user.id, page=page, page_size=page_size
    )
    return Result.success(data=data)


@router.put("/{borrow_id}/audit")
async def audit_borrow(
    borrow_id: int,
    req: BorrowAuditRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    service = BorrowService(db)
    borrow = await service.audit_borrow(borrow_id, req, current_user.id)
    return Result.success(data=borrow, msg="审核完成")


@router.put("/{borrow_id}/return")
async def return_borrow(
    borrow_id: int,
    req: BorrowReturnRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = BorrowService(db)
    borrow = await service.return_borrow(borrow_id, req, current_user.id)
    return Result.success(data=borrow, msg="归还申请已提交")


@router.put("/{borrow_id}/confirm-return")
async def confirm_return(
    borrow_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    service = BorrowService(db)
    await service.confirm_return(borrow_id, current_user.id)
    return Result.success(msg="归还已确认")