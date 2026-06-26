from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.borrow_repo import BorrowRepository
from app.repositories.device_repo import DeviceRepository
from app.repositories.audit_repo import AuditRepository
from app.models.borrow import Borrow, BorrowStatus, ReturnStatus
from app.models.device import DeviceStatus
from app.models.audit import AuditLog
from app.schemas.borrow import (
    BorrowCreateRequest,
    BorrowAuditRequest,
    BorrowReturnRequest,
)


class BorrowService:
    def __init__(self, db: AsyncSession):
        self.repo = BorrowRepository(db)
        self.device_repo = DeviceRepository(db)
        self.audit_repo = AuditRepository(db)

    async def create_borrow(self, req: BorrowCreateRequest, user_id: int):
        # 检查设备是否存在
        device = await self.device_repo.get_by_id(req.device_id)
        if not device:
            raise HTTPException(status_code=404, detail="设备不存在")
        # 检查设备是否可借用
        if device.status != DeviceStatus.available:
            raise HTTPException(status_code=409, detail="设备当前不可借用")

        borrow = Borrow(
            device_id=req.device_id,
            user_id=user_id,
            status=BorrowStatus.pending,
            borrow_reason=req.borrow_reason,
            expected_return_time=(
                datetime.fromisoformat(req.expected_return_time)
                if req.expected_return_time
                else None
            ),
        )

        # 更新设备状态为待审核
        device.status = DeviceStatus.pending_borrow
        await self.device_repo.update(device)

        result = await self.repo.create(borrow)

        # 记录审核日志
        audit_log = AuditLog(
            target_type="borrow",
            target_id=result.id,
            action="create",
            from_status=None,
            to_status=BorrowStatus.pending.value,
            operator_id=user_id,
            remark=req.borrow_reason,
        )
        await self.audit_repo.create(audit_log)

        return result

    async def audit_borrow(
        self, borrow_id: int, req: BorrowAuditRequest, auditor_id: int
    ):
        borrow = await self.repo.get_by_id(borrow_id)
        if not borrow:
            raise HTTPException(status_code=404, detail="借用记录不存在")
        if borrow.status != BorrowStatus.pending:
            raise HTTPException(status_code=409, detail="该借用申请已处理")

        device = await self.device_repo.get_by_id(borrow.device_id)

        if req.action == "approve":
            borrow.status = BorrowStatus.borrowing
            borrow.borrow_time = datetime.now()
            borrow.audit_by = auditor_id
            borrow.audit_time = datetime.now()
            borrow.audit_remark = req.remark
            device.status = DeviceStatus.borrowed
        elif req.action == "reject":
            borrow.status = BorrowStatus.rejected
            borrow.audit_by = auditor_id
            borrow.audit_time = datetime.now()
            borrow.audit_remark = req.remark
            device.status = DeviceStatus.available
        else:
            raise HTTPException(
                status_code=400, detail="无效的操作，请使用 approve 或 reject"
            )

        await self.device_repo.update(device)
        result = await self.repo.update(borrow)

        # 记录审核日志
        audit_log = AuditLog(
            target_type="borrow",
            target_id=borrow_id,
            action=req.action,
            from_status=BorrowStatus.pending.value,
            to_status=borrow.status.value,
            operator_id=auditor_id,
            remark=req.remark,
        )
        await self.audit_repo.create(audit_log)

        return result

    async def return_borrow(
        self, borrow_id: int, req: BorrowReturnRequest, user_id: int
    ):
        borrow = await self.repo.get_by_id(borrow_id)
        if not borrow:
            raise HTTPException(status_code=404, detail="借用记录不存在")
        if borrow.user_id != user_id:
            raise HTTPException(status_code=403, detail="只能归还自己的借用记录")
        if borrow.status != BorrowStatus.borrowing:
            raise HTTPException(status_code=409, detail="当前状态不支持归还操作")

        device = await self.device_repo.get_by_id(borrow.device_id)

        from_status = borrow.status.value

        borrow.return_status = ReturnStatus(req.return_status)
        borrow.actual_return_time = datetime.now()

        if req.return_status == "damaged":
            borrow.damage_description = req.damage_description
            borrow.status = BorrowStatus.damaged_returned
            device.status = DeviceStatus.damaged
        else:
            borrow.status = BorrowStatus.pending_return
            device.status = DeviceStatus.pending_return

        await self.device_repo.update(device)
        result = await self.repo.update(borrow)

        # 记录审核日志
        audit_log = AuditLog(
            target_type="borrow",
            target_id=borrow_id,
            action="return",
            from_status=from_status,
            to_status=borrow.status.value,
            operator_id=user_id,
            remark=req.damage_description if req.return_status == "damaged" else None,
        )
        await self.audit_repo.create(audit_log)

        return result

    async def confirm_return(self, borrow_id: int, admin_id: int):
        borrow = await self.repo.get_by_id(borrow_id)
        if not borrow:
            raise HTTPException(status_code=404, detail="借用记录不存在")
        if borrow.status != BorrowStatus.pending_return:
            raise HTTPException(status_code=409, detail="当前状态不支持确认归还")

        device = await self.device_repo.get_by_id(borrow.device_id)
        device.status = DeviceStatus.available
        await self.device_repo.update(device)

        # 记录审核日志
        audit_log = AuditLog(
            target_type="borrow",
            target_id=borrow_id,
            action="confirm_return",
            from_status=BorrowStatus.pending_return.value,
            to_status=BorrowStatus.returned.value,
            operator_id=admin_id,
            remark="管理员确认归还",
        )
        await self.audit_repo.create(audit_log)

        borrow.status = BorrowStatus.returned
        return await self.repo.update(borrow)

    async def get_borrows(
        self, page: int = 1, page_size: int = 10, status: str = None
    ):
        return await self.repo.get_list(
            page=page, page_size=page_size, status=status
        )

    async def get_my_borrows(
        self, user_id: int, page: int = 1, page_size: int = 10
    ):
        return await self.repo.get_by_user(
            user_id=user_id, page=page, page_size=page_size
        )