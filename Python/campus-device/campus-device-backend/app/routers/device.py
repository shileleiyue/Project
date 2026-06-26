from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.models import get_db
from app.dependencies import get_current_user, require_role
from app.schemas.device import DeviceCreateRequest, DeviceUpdateRequest
from app.services.device_service import DeviceService
from app.utils.response_util import Result

router = APIRouter()


def _serialize_device(device):
    """将设备模型序列化为字典，排除敏感信息"""
    return {
        "id": device.id,
        "name": device.name,
        "type": device.type,
        "description": device.description,
        "image": device.image,
        "status": device.status.value if hasattr(device.status, 'value') else device.status,
        "location": device.location,
        "created_by": device.created_by,
        "created_at": device.created_at.isoformat() if device.created_at else None,
        "updated_at": device.updated_at.isoformat() if device.updated_at else None,
        "creator": {
            "id": device.creator.id,
            "username": device.creator.username,
            "phone": device.creator.phone,
            "role": device.creator.role.value if hasattr(device.creator.role, 'value') else device.creator.role,
        } if device.creator else None,
    }

@router.get("")
async def get_devices(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: Optional[str] = None,
    type: Optional[str] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = DeviceService(db)
    data = await service.get_devices(page=page, page_size=page_size, keyword=keyword, type=type, status=status)
    # 序列化设备列表
    if data and "list" in data:
        data["list"] = [_serialize_device(d) for d in data["list"]]
    return Result.success(data=data)

@router.get("/{device_id}")
async def get_device(
    device_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = DeviceService(db)
    device = await service.get_device(device_id)
    return Result.success(data=_serialize_device(device))

@router.post("")
async def create_device(
    req: DeviceCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    service = DeviceService(db)
    device = await service.create_device(req, current_user.id)
    return Result.success(data=_serialize_device(device), msg="设备创建成功")

@router.put("/{device_id}")
async def update_device(
    device_id: int,
    req: DeviceUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    service = DeviceService(db)
    device = await service.update_device(device_id, req)
    return Result.success(data=_serialize_device(device), msg="设备更新成功")

@router.put("/{device_id}/offline")
async def offline_device(
    device_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    service = DeviceService(db)
    device = await service.offline_device(device_id)
    return Result.success(data=_serialize_device(device), msg="设备已下架")

@router.delete("/{device_id}")
async def delete_device(
    device_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    service = DeviceService(db)
    await service.delete_device(device_id)
    return Result.success(msg="设备已删除")