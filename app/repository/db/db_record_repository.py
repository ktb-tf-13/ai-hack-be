from sqlalchemy.orm import Session
from sqlalchemy import select
import app.model.models as models
from app.schema.record_schema import RecordRequest

class RecordRepositoryDB:
    def __init__(self, db: Session):
        self.db = db

    def upsert_record(self, request: RecordRequest):
        # 해당 유저의 해당 날짜 기록이 있는지 조회
        stmt = select(models.Record).where(
            models.Record.user_id == request.user_id,
            models.Record.record_date == request.date
        )
        existing_record = self.db.execute(stmt).scalar_one_or_none()

        if existing_record:
            # [CASE 1] 이미 있으면 -> 내용 업데이트 (덮어쓰기)
            existing_record.record_content = request.content
            existing_record.record_is_written = True # 작성됨 표시
            
            # 여기서 date는 바꿀 필요 없으므로 생략 (검색 조건과 같음)
            
            self.db.commit()
            self.db.refresh(existing_record)
            return existing_record

        else:
            # [CASE 2] 없으면 -> 새로 생성 (Insert)
            new_record = models.Record(
                user_id=request.user_id,
                record_content=request.content,
                record_date=request.date,
                record_is_written=True
            )
            
            self.db.add(new_record)
            self.db.commit()
            self.db.refresh(new_record)
            return new_record
        
    def get_record(self, user_id: int, target_date: str):
        # SELECT * FROM Record WHERE user_id = ... AND record_date = ...
        stmt = select(models.Record).where(
            models.Record.user_id == user_id,
            models.Record.record_date == target_date
        )
        return self.db.execute(stmt).scalar_one_or_none()