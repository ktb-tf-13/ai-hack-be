from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schema.record_schema import RecordRequest, RecordSearchRequest
from app.repository.db.db_record_repository import RecordRepositoryDB
from app.core.exception import CustomException, ErrorCode

router = APIRouter()

@router.put("/records")
async def write_record(request: RecordRequest, db: AsyncSession = Depends(get_db)):
    repo = RecordRepositoryDB(db)
    
    # [방어 로직] 유저가 존재하는지 먼저 확인!
    if not await repo.check_user_exists(request.user_id):
        # 유저가 없으면 에러
        raise CustomException(
            code=ErrorCode.USER_NOT_FOUND, # 아까 정의한 코드
            message=f"ID가 {request.user_id}인 사용자를 찾을 수 없습니다."
        )

    result_record = await repo.upsert_record(request)
    
    return {
        "id": result_record.record_id,
        "content": result_record.record_content,
        "date": result_record.record_date
    }

#기록 조회 
@router.post("/records")
async def get_record(request: RecordSearchRequest, db: AsyncSession = Depends(get_db)):
    repo = RecordRepositoryDB(db)
    
    # 레포지토리에서 조회
    record = await repo.get_record(user_id=request.user_id, target_date=request.date)
    
    # 기록이 없을 경우 예외 처리 (404 Not Found)
    if not record:
        return {
            "id": None,          # ID가 없으므로 null 반환
            "content": "",       # 요청하신 대로 빈 문자열
            "date": request.date # 요청한 날짜는 그대로 돌려줌 (프론트 편의성)
        }

    # 기록이 있으면 응답 반환
    return {
        "id": record.record_id,
        "content": record.record_content,
        "date": record.record_date
    }