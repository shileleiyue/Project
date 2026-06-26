from fastapi import APIRouter, Depends, Query, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.models import get_db
from app.dependencies import get_current_user, require_role
from app.schemas.repair import RepairCreateRequest, RepairAssignRequest, RepairStatusUpdateRequest
from app.services.repair_service import RepairService
from app.utils.response_util import Result

router = APIRouter()


@router.post("")
async def create_repair(
    req: RepairCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    service = RepairService(db)
    repair = await service.create_repair(req, current_user.id)
    return Result.success(data=repair, msg="维修工单已创建")


@router.get("")
async def get_repairs(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    service = RepairService(db)
    data = await service.get_repairs(page=page, page_size=page_size, status=status)
    return Result.success(data=data)


@router.get("/my")
async def get_my_repairs(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = RepairService(db)
    data = await service.get_my_repairs(current_user.id, page=page, page_size=page_size)
    return Result.success(data=data)


@router.get("/assigned")
async def get_assigned_repairs(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("repairer"))
):
    service = RepairService(db)
    data = await service.get_assigned_repairs(current_user.id, page=page, page_size=page_size)
    return Result.success(data=data)


@router.get("/{repair_id}")
async def get_repair(
    repair_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = RepairService(db)
    repair = await service.get_repair(repair_id)
    return Result.success(data=repair)


@router.put("/{repair_id}/assign")
async def assign_repair(
    repair_id: int,
    req: RepairAssignRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    service = RepairService(db)
    repair = await service.assign_repair(repair_id, req, current_user.id)
    return Result.success(data=repair, msg="维修人员已分配")


@router.put("/{repair_id}/status")
async def update_repair_status(
    repair_id: int,
    req: RepairStatusUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("repairer"))
):
    service = RepairService(db)
    repair = await service.update_status(repair_id, req, current_user.id)
    return Result.success(data=repair, msg="状态已更新")


@router.put("/{repair_id}/confirm")
async def confirm_repair(
    repair_id: int,
    action: str = Query("complete", description="complete 或 scrap"),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    service = RepairService(db)
    repair = await service.confirm_repair(repair_id, current_user.id, action)
    msg = "设备已报废" if action == "scrap" else "维修已完成"
    return Result.success(data=repair, msg=msg)


@router.post("/{repair_id}/images")
async def upload_repair_images(
    repair_id: int,
    files: List[UploadFile] = File(...),
    image_type: str = Form("damage"),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = RepairService(db)
    images = []
    for file in files:
        image = await service.upload_image(repair_id, file, image_type, current_user.id)
        images.append(image)
    return Result.success(data=images, msg="图片上传成功")