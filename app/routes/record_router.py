from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schema.record_schema import RecordRequest, RecordSearchRequest
from app.repository.db_record_repository import RecordRepositoryDB

router = APIRouter()

@router.put("/records")
def write_record(request: RecordRequest, db: Session = Depends(get_db)):
    repo = RecordRepositoryDB(db)
    
    # Upsert 실행
    result_record = repo.upsert_record(request)
    
    return {
        "id": result_record.record_id,
        "content": result_record.record_content,
        "date": result_record.record_date
    }

#기록 조회 
@router.post("/records")
def get_record(request: RecordSearchRequest, db: Session = Depends(get_db)):
    repo = RecordRepositoryDB(db)
    
    # 레포지토리에서 조회
    record = repo.get_record(user_id=request.user_id, target_date=request.date)
    
    # 기록이 없을 경우 예외 처리 (404 Not Found)
    if not record:
        raise HTTPException(status_code=404, detail="해당 날짜의 기록을 찾을 수 없습니다.")
    
    # 기록이 있으면 응답 반환
    return {
        "id": record.record_id,
        "content": record.record_content,
        "date": record.record_date
    }