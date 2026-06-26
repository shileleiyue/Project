from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit import AuditLog

class AuditRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, audit_log: AuditLog) -> AuditLog:
        self.db.add(audit_log)
        await self.db.flush()
        await self.db.refresh(audit_log)
        return audit_log

    async def get_by_target(self, target_type: str, target_id: int, page: int = 1, page_size: int = 10):
        query = select(AuditLog).where(
            AuditLog.target_type == target_type,
            AuditLog.target_id == target_id
        ).order_by(AuditLog.created_at.desc())

        count_query = select(func.count(AuditLog.id)).where(
            AuditLog.target_type == target_type,
            AuditLog.target_id == target_id
        )

        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        result = await self.db.execute(query)
        logs = result.scalars().all()

        return {
            "list": logs,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(1, (total + page_size - 1) // page_size)
        }