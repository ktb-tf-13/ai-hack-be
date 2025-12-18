from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession # [수정] Import 변경
from app.core.database import get_db
from app.schema.record_schema import RecordRequest, RecordSearchRequest
from app.repository.db.db_record_repository import RecordRepositoryDB
from app.core.exception import CustomException, ErrorCode

router = APIRouter()

@router.put("/records")
async def write_record(request: RecordRequest, db: AsyncSession = Depends(get_db)):
    repo = RecordRepositoryDB(db)
    
    if not await repo.check_user_exists(request.user_id):
        raise CustomException(
            code=ErrorCode.USER_NOT_FOUND,
            message=f"ID가 {request.user_id}인 사용자를 찾을 수 없습니다."
        )

    result_record = await repo.upsert_record(request)
    
    return {
        "id": result_record.record_id,
        "content": result_record.record_content,
        "date": result_record.record_date
    }

# 기록 조회 
@router.post("/records")
async def get_record(request: RecordSearchRequest, db: AsyncSession = Depends(get_db)):
    repo = RecordRepositoryDB(db)
    
    record = await repo.get_record(user_id=request.user_id, target_date=request.date)
    
    if not record:
        return {
            "id": None,
            "content": "",
            "date": request.date
        }

    return {
        "id": record.record_id,
        "content": record.record_content,
        "date": record.record_date
    }