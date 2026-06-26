from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.device_repo import DeviceRepository
from app.models.device import Device, DeviceStatus
from app.schemas.device import DeviceCreateRequest, DeviceUpdateRequest

class DeviceService:
    def __init__(self, db: AsyncSession):
        self.repo = DeviceRepository(db)

    async def get_device(self, device_id: int):
        device = await self.repo.get_by_id(device_id)
        if not device:
            raise HTTPException(status_code=404, detail="设备不存在")
        return device

    async def get_devices(self, page: int = 1, page_size: int = 10, keyword: str = None, type: str = None, status: str = None):
        result = await self.repo.get_list(page=page, page_size=page_size, keyword=keyword, type=type, status=status)
        return result

    async def create_device(self, req: DeviceCreateRequest, user_id: int):
        device = Device(
            name=req.name,
            type=req.type,
            description=req.description,
            location=req.location,
            image=req.image,
            status=DeviceStatus.available,
            created_by=user_id
        )
        return await self.repo.create(device)

    async def update_device(self, device_id: int, req: DeviceUpdateRequest):
        device = await self.get_device(device_id)
        if req.name is not None:
            device.name = req.name
        if req.type is not None:
            device.type = req.type
        if req.description is not None:
            device.description = req.description
        if req.location is not None:
            device.location = req.location
        if req.image is not None:
            device.image = req.image
        return await self.repo.update(device)

    async def offline_device(self, device_id: int):
        device = await self.get_device(device_id)
        if device.status == DeviceStatus.offline:
            raise HTTPException(status_code=409, detail="设备已下架")
        if device.status == DeviceStatus.borrowed:
            raise HTTPException(status_code=409, detail="设备正在借用中，无法下架")
        device.status = DeviceStatus.offline
        return await self.repo.update(device)

    async def delete_device(self, device_id: int):
        device = await self.get_device(device_id)
        if device.status == DeviceStatus.borrowed:
            raise HTTPException(status_code=409, detail="设备正在借用中，无法删除")
        await self.repo.delete(device)