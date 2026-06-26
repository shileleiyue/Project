from datetime import datetime
from fastapi import HTTPException, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.repair_repo import RepairRepository
from app.repositories.device_repo import DeviceRepository
from app.repositories.audit_repo import AuditRepository
from app.models.repair import Repair, RepairImage, RepairStatus, RepairImageType
from app.models.device import DeviceStatus
from app.models.user import UserRole
from app.models.audit import AuditLog
from app.schemas.repair import RepairCreateRequest, RepairAssignRequest, RepairStatusUpdateRequest
from app.utils.file_util import save_upload_file, validate_image


class RepairService:
    def __init__(self, db: AsyncSession):
        self.repo = RepairRepository(db)
        self.device_repo = DeviceRepository(db)
        self.audit_repo = AuditRepository(db)

    async def create_repair(self, req: RepairCreateRequest, admin_id: int):
        device = await self.device_repo.get_by_id(req.device_id)
        if not device:
            raise HTTPException(status_code=404, detail="设备不存在")
        if device.status not in (DeviceStatus.available, DeviceStatus.damaged):
            raise HTTPException(status_code=409, detail="设备当前状态无法创建维修工单")

        repair = Repair(
            device_id=req.device_id,
            borrow_id=req.borrow_id,
            reporter_id=admin_id,
            status=RepairStatus.pending,
            fault_description=req.fault_description
        )

        device.status = DeviceStatus.repair_pending
        await self.device_repo.update(device)

        result = await self.repo.create(repair)

        # 记录审核日志
        audit_log = AuditLog(
            target_type="repair",
            target_id=result.id,
            action="create",
            from_status=None,
            to_status=RepairStatus.pending.value,
            operator_id=admin_id,
            remark=req.fault_description,
        )
        await self.audit_repo.create(audit_log)

        return result

    async def assign_repair(self, repair_id: int, req: RepairAssignRequest, admin_id: int):
        repair = await self.repo.get_by_id(repair_id)
        if not repair:
            raise HTTPException(status_code=404, detail="工单不存在")
        if repair.status != RepairStatus.pending:
            raise HTTPException(status_code=409, detail="当前状态不支持分配")

        repair.assigned_to = req.assigned_to
        repair.status = RepairStatus.assigned
        result = await self.repo.update(repair)

        # 记录审核日志
        audit_log = AuditLog(
            target_type="repair",
            target_id=repair_id,
            action="assign",
            from_status=RepairStatus.pending.value,
            to_status=RepairStatus.assigned.value,
            operator_id=admin_id,
            remark=f"分配给维修人员 {req.assigned_to}"
        )
        await self.audit_repo.create(audit_log)

        return result

    async def update_status(self, repair_id: int, req: RepairStatusUpdateRequest, user_id: int):
        repair = await self.repo.get_by_id(repair_id)
        if not repair:
            raise HTTPException(status_code=404, detail="工单不存在")
        if repair.assigned_to != user_id:
            raise HTTPException(status_code=403, detail="只能更新分配给自己的工单")

        device = await self.device_repo.get_by_id(repair.device_id)

        from_status = repair.status.value

        if req.status == "repairing":
            repair.status = RepairStatus.repairing
            device.status = DeviceStatus.repairing
        elif req.status == "repaired":
            repair.status = RepairStatus.repaired
            repair.repair_process = req.repair_process
            repair.repair_result = req.repair_result
            device.status = DeviceStatus.repaired
        elif req.status == "unfixable":
            repair.status = RepairStatus.unfixable
            repair.repair_result = req.repair_result
        else:
            raise HTTPException(status_code=400, detail="无效的状态")

        await self.device_repo.update(device)
        result = await self.repo.update(repair)

        # 记录审核日志
        audit_log = AuditLog(
            target_type="repair",
            target_id=repair_id,
            action=req.status,
            from_status=from_status,
            to_status=repair.status.value,
            operator_id=user_id,
            remark=req.repair_result,
        )
        await self.audit_repo.create(audit_log)

        return result

    async def confirm_repair(self, repair_id: int, admin_id: int, action: str = "complete"):
        repair = await self.repo.get_by_id(repair_id)
        if not repair:
            raise HTTPException(status_code=404, detail="工单不存在")
        if action == "scrap" and repair.status != RepairStatus.unfixable:
            raise HTTPException(status_code=409, detail="只有标记为无法修复的工单才能报废")
        if action != "scrap" and repair.status != RepairStatus.repaired:
            raise HTTPException(status_code=409, detail="当前状态不支持确认")

        device = await self.device_repo.get_by_id(repair.device_id)

        if action == "scrap":
            repair.status = RepairStatus.completed
            repair.is_confirmed = True
            repair.confirmed_by = admin_id
            repair.confirmed_at = datetime.now()
            device.status = DeviceStatus.scrapped
        else:
            repair.status = RepairStatus.completed
            repair.is_confirmed = True
            repair.confirmed_by = admin_id
            repair.confirmed_at = datetime.now()
            device.status = DeviceStatus.available

        await self.device_repo.update(device)
        result = await self.repo.update(repair)

        # 记录审核日志
        audit_log = AuditLog(
            target_type="repair",
            target_id=repair_id,
            action="confirm" if action != "scrap" else "scrap",
            from_status=RepairStatus.repaired.value,
            to_status=RepairStatus.completed.value,
            operator_id=admin_id,
            remark="报废处理" if action == "scrap" else "确认完成",
        )
        await self.audit_repo.create(audit_log)

        return result

    async def upload_image(self, repair_id: int, file: UploadFile, image_type: str, user_id: int):
        repair = await self.repo.get_by_id(repair_id)
        if not repair:
            raise HTTPException(status_code=404, detail="工单不存在")

        # 校验图片
        validate_image(file)

        # 保存文件
        sub_dir = "repair" if image_type in ("before_repair", "after_repair") else "damage"
        file_path = await save_upload_file(file, sub_dir)

        image = RepairImage(
            repair_id=repair_id,
            image_type=RepairImageType(image_type),
            image_path=file_path,
            uploaded_by=user_id
        )

        return await self.repo.add_image(image)

    async def get_repairs(self, page: int = 1, page_size: int = 10, status: str = None):
        return await self.repo.get_list(page=page, page_size=page_size, status=status)

    async def get_my_repairs(self, user_id: int, page: int = 1, page_size: int = 10):
        return await self.repo.get_by_reporter(user_id=user_id, page=page, page_size=page_size)

    async def get_assigned_repairs(self, user_id: int, page: int = 1, page_size: int = 10):
        return await self.repo.get_by_assignee(user_id=user_id, page=page, page_size=page_size)

    async def get_repair(self, repair_id: int):
        repair = await self.repo.get_by_id(repair_id)
        if not repair:
            raise HTTPException(status_code=404, detail="工单不存在")
        return repair