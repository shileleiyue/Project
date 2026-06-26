from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.models.borrow import Borrow, BorrowStatus


class BorrowRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, borrow_id: int) -> Optional[Borrow]:
        result = await self.db.execute(
            select(Borrow)
            .options(joinedload(Borrow.device), joinedload(Borrow.user))
            .where(Borrow.id == borrow_id)
        )
        return result.scalar_one_or_none()

    async def get_list(
        self, page: int = 1, page_size: int = 10, status: Optional[str] = None
    ):
        query = select(Borrow).options(
            joinedload(Borrow.device), joinedload(Borrow.user)
        )
        count_query = select(func.count(Borrow.id))

        if status:
            query = query.where(Borrow.status == status)
            count_query = count_query.where(Borrow.status == status)

        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size).order_by(Borrow.id.desc())

        result = await self.db.execute(query)
        borrows = result.scalars().all()

        return {
            "list": borrows,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(1, (total + page_size - 1) // page_size),
        }

    async def get_by_user(
        self, user_id: int, page: int = 1, page_size: int = 10
    ):
        query = (
            select(Borrow)
            .options(joinedload(Borrow.device))
            .where(Borrow.user_id == user_id)
        )
        count_query = select(func.count(Borrow.id)).where(Borrow.user_id == user_id)

        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size).order_by(Borrow.id.desc())

        result = await self.db.execute(query)
        borrows = result.scalars().all()

        return {
            "list": borrows,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(1, (total + page_size - 1) // page_size),
        }

    async def create(self, borrow: Borrow) -> Borrow:
        self.db.add(borrow)
        await self.db.flush()
        await self.db.refresh(borrow)
        return borrow

    async def update(self, borrow: Borrow) -> Borrow:
        await self.db.flush()
        await self.db.refresh(borrow)
        return borrow