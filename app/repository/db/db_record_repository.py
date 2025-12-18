from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
import app.model.models as models
from app.schema.record_schema import RecordRequest

class RecordRepositoryDB:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def check_user_exists(self, user_id: int) -> bool:
        stmt = select(exists().where(models.User.user_id == user_id))
        result = await self.db.execute(stmt)
        return result.scalar()

    async def upsert_record(self, request: RecordRequest):
        stmt = select(models.Record).where(
            models.Record.user_id == request.user_id,
            models.Record.record_date == request.date
        )
        result = await self.db.execute(stmt)
        existing_record = result.scalar_one_or_none()

        if existing_record:
            # [CASE 1] 업데이트
            existing_record.record_content = request.content
            existing_record.record_is_wrote = True
            
            await self.db.commit()
            await self.db.refresh(existing_record)
            return existing_record

        else:
            # [CASE 2] 생성
            new_record = models.Record(
                user_id=request.user_id,
                record_content=request.content,
                record_date=request.date,
                record_is_wrote=True
            )
            
            # 주의: db.add()는 동기 메서드라 await 안 붙임 (SQLAlchemy 특성)
            self.db.add(new_record)
            
            await self.db.commit()
            await self.db.refresh(new_record)
            return new_record
        
    async def get_record(self, user_id: int, target_date: str):
        stmt = select(models.Record).where(
            models.Record.user_id == user_id,
            models.Record.record_date == target_date
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()