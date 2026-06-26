from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.models.repair import Repair, RepairImage, RepairStatus


class RepairRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, repair_id: int) -> Optional[Repair]:
        result = await self.db.execute(
            select(Repair)
            .options(
                joinedload(Repair.device),
                joinedload(Repair.reporter),
                joinedload(Repair.assignee),
                joinedload(Repair.images)
            )
            .where(Repair.id == repair_id)
        )
        return result.unique().scalar_one_or_none()

    async def get_list(self, page: int = 1, page_size: int = 10, status: Optional[str] = None):
        query = select(Repair).options(
            joinedload(Repair.device),
            joinedload(Repair.reporter),
            joinedload(Repair.assignee)
        )
        count_query = select(func.count(Repair.id))

        if status:
            query = query.where(Repair.status == status)
            count_query = count_query.where(Repair.status == status)

        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size).order_by(Repair.id.desc())

        result = await self.db.execute(query)
        repairs = result.unique().scalars().all()

        return {
            "list": repairs,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(1, (total + page_size - 1) // page_size)
        }

    async def get_by_reporter(self, user_id: int, page: int = 1, page_size: int = 10):
        query = select(Repair).options(
            joinedload(Repair.device),
            joinedload(Repair.assignee)
        ).where(Repair.reporter_id == user_id)

        count_query = select(func.count(Repair.id)).where(Repair.reporter_id == user_id)

        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size).order_by(Repair.id.desc())

        result = await self.db.execute(query)
        repairs = result.unique().scalars().all()

        return {
            "list": repairs,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(1, (total + page_size - 1) // page_size)
        }

    async def get_by_assignee(self, user_id: int, page: int = 1, page_size: int = 10):
        query = select(Repair).options(
            joinedload(Repair.device),
            joinedload(Repair.reporter)
        ).where(Repair.assigned_to == user_id)

        count_query = select(func.count(Repair.id)).where(Repair.assigned_to == user_id)

        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size).order_by(Repair.id.desc())

        result = await self.db.execute(query)
        repairs = result.unique().scalars().all()

        return {
            "list": repairs,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(1, (total + page_size - 1) // page_size)
        }

    async def create(self, repair: Repair) -> Repair:
        self.db.add(repair)
        await self.db.flush()
        await self.db.refresh(repair)
        return repair

    async def update(self, repair: Repair) -> Repair:
        await self.db.flush()
        await self.db.refresh(repair)
        return repair

    async def add_image(self, image: RepairImage) -> RepairImage:
        self.db.add(image)
        await self.db.flush()
        await self.db.refresh(image)
        return image