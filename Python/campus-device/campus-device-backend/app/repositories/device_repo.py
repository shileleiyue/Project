from typing import Optional
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.device import Device, DeviceStatus

class DeviceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, device_id: int) -> Optional[Device]:
        result = await self.db.execute(select(Device).where(Device.id == device_id))
        return result.scalar_one_or_none()

    async def get_list(self, page: int = 1, page_size: int = 10, keyword: Optional[str] = None, type: Optional[str] = None, status: Optional[str] = None):
        query = select(Device)
        count_query = select(func.count(Device.id))

        if keyword:
            filter_cond = Device.name.contains(keyword)
            query = query.where(filter_cond)
            count_query = count_query.where(filter_cond)

        if type:
            query = query.where(Device.type == type)
            count_query = count_query.where(Device.type == type)

        if status:
            query = query.where(Device.status == status)
            count_query = count_query.where(Device.status == status)

        # 获取总数
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        # 分页
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size).order_by(Device.id.desc())

        result = await self.db.execute(query)
        devices = result.scalars().all()

        return {
            "list": devices,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(1, (total + page_size - 1) // page_size)
        }

    async def create(self, device: Device) -> Device:
        self.db.add(device)
        await self.db.flush()
        await self.db.refresh(device)
        return device

    async def update(self, device: Device) -> Device:
        await self.db.flush()
        await self.db.refresh(device)
        return device

    async def delete(self, device: Device):
        await self.db.delete(device)
        await self.db.flush()