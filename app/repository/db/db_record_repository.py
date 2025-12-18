from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
import app.model.models as models
from app.schema.record_schema import RecordRequest

class RecordRepositoryDB:
    def __init__(self, db: AsyncSession):
        self.db = db

    # 유저 존재 여부 확인
    async def check_user_exists(self, user_id: str) -> bool:
        stmt = select(exists().where(models.User.user_id == user_id))
        result = await self.db.execute(stmt)
        return result.scalar()

    async def upsert_record(self, request: RecordRequest):
        # 해당 유저의 해당 날짜 기록이 있는지 조회
        stmt = select(models.Record).where(
            models.Record.user_id == request.user_id,
            models.Record.record_date == request.date
        )
        result = await self.db.execute(stmt)
        existing_record = result.scalar_one_or_none()

        if existing_record:
            # [CASE 1] 이미 있으면 -> 내용 업데이트 (덮어쓰기)
            existing_record.record_content = request.content
            # models.py에 정의된 필드명은 record_is_wrote 임 (아까 보니까)
            # 하지만 여기서는 record_is_written을 쓰고 있음 -> models.py 확인 필요.
            # 일단 models.Record class definition을 보면 record_is_wrote 임.
            # 사용자가 코드를 작성했음. -> models.py에 맞게 수정 필요.
            # models.py: record_is_wrote = Column(Boolean, default=False, nullable=False)
            existing_record.record_is_wrote = True 
            
            await self.db.commit()
            await self.db.refresh(existing_record)
            return existing_record

        else:
            # [CASE 2] 없으면 -> 새로 생성 (Insert)
            new_record = models.Record(
                user_id=request.user_id,
                record_content=request.content,
                record_date=request.date,
                record_is_wrote=True
            )
            
            self.db.add(new_record)
            await self.db.commit()
            await self.db.refresh(new_record)
            return new_record
        
    async def get_record(self, user_id: str, target_date: str):
        # SELECT * FROM Record WHERE user_id = ... AND record_date = ...
        stmt = select(models.Record).where(
            models.Record.user_id == user_id,
            models.Record.record_date == target_date
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()