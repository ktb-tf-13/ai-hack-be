from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List, Optional
from datetime import date
from app.model.models import Record

class RecordRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_recent_records(self, user_id: str, limit: int = 10) -> List[Record]:
        result = await self.db.execute(
            select(Record)
            .where(Record.user_id == user_id)
            .order_by(Record.record_date.desc())
            .limit(limit)
        )
        return result.scalars().all()
