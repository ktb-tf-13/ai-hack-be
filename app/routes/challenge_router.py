from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schema.challenge_schema import (
    ChallengeRequest, 
    ChallengeCompleteRequest, 
    ChallengeCancelRequest,
    ChallengeDeleteRequest,
    ChallengeWeeklyStatsRequest,
    ChallengeWeeklyStatsResponse,
    DailyStat
)
from datetime import datetime, timedelta

from app.repository.db.db_challenge_repository import ChallengeRepositoryDB


router = APIRouter()

@router.post("/challenges")
async def get_challenges(request: ChallengeRequest, db: AsyncSession = Depends(get_db)):
    
    # 로직
    # 들어온 요청 값(request.user_id 등)을 로그로 확인해볼 수 있습니다.
    print(f"DEBUG: 요청 들어옴 - user_id: {request.user_id}, date: {request.date}")

    repo = ChallengeRepositoryDB(db)
    # user_id는 DB에서 String으로 관리
    challenges = await repo.get_challenges(request.user_id, request.date)

    return {
        "challenges": [
            {
                "id": c.challenge_id,
                "user_id": c.user_id,
                "content": c.challenge_content,
                "is_checked": c.challenge_is_checked,
                "date": c.challenge_date,       
            }
            for c in challenges
        ]
    }

# 챌린지 완료
@router.post("/users/challenges/complete")
async def complete_challenge(request: ChallengeCompleteRequest, db: AsyncSession = Depends(get_db)):
    
    print(f"DEBUG: 챌린지 완료 요청됨 - ID: {request.id}, User: {request.user_id}, Date: {request.date}")

    repo = ChallengeRepositoryDB(db)
    # 완료 상태(True)로 업데이트
    result = await repo.update_challenge_status(int(request.id), request.user_id, request.date, True)
    
    return result

# 챌린지 완료 취소
@router.post("/users/challenges/cancel")
async def cancel_challenge(request: ChallengeCancelRequest, db: AsyncSession = Depends(get_db)):
    
    print(f"DEBUG: 챌린지 취소 요청됨 - ID: {request.id}, User: {request.user_id}, Date: {request.date}")

    repo = ChallengeRepositoryDB(db)
    # 완료 취소 상태(False)로 업데이트
    result = await repo.update_challenge_status(int(request.id), request.user_id, request.date, False)

    return result

# 챌린지 삭제
@router.delete("/users/challenges/delete")
async def delete_challenge(request: ChallengeDeleteRequest, db: AsyncSession = Depends(get_db)):
    
    print(f"DEBUG: 챌린지 삭제 요청됨 - ID: {request.id}")

    repo = ChallengeRepositoryDB(db)
    result = await repo.delete_challenge(request.id)
    
    return {
        "id": request.id,
        "is_deleted": True,
        "message": "챌린지가 성공적으로 삭제되었습니다."
    }

@router.post("/challenges/weekly-stats", response_model=ChallengeWeeklyStatsResponse)
async def get_weekly_challenge_stats(request: ChallengeWeeklyStatsRequest, db: AsyncSession = Depends(get_db)):
    repo = ChallengeRepositoryDB(db)
    
    # Date parsing
    try:
        target_date = datetime.strptime(request.date, "%Y%m%d").date()
    except ValueError:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYYMMDD")

    # Calculate Monday and Sunday of the week
    start_of_week = target_date - timedelta(days=target_date.weekday()) # Monday
    end_of_week = start_of_week + timedelta(days=6) # Sunday
    
    # Initialize daily stats structure
    # weekday(): 0=Mon, 6=Sun
    daily_stats_map = {}
    korean_days = ["월", "화", "수", "목", "금", "토", "일"]
    
    for i in range(7):
        current_day = start_of_week + timedelta(days=i)
        day_str = f"{current_day.month}.{current_day.day}({korean_days[i]})"
        daily_stats_map[current_day] = {
            "date": day_str,
            "total": 0,
            "success": 0
        }

    # Fetch challenges
    challenges = await repo.get_challenges_by_period(request.user_id, start_of_week, end_of_week)
    
    total_challenges = 0
    total_success = 0
    
    for ch in challenges:
        c_date = ch.challenge_date
        # Ensure date is key (might be string or date obj depending on DB driver, usually date obj)
        if c_date in daily_stats_map:
            daily_stats_map[c_date]["total"] += 1
            if ch.challenge_is_checked:
                daily_stats_map[c_date]["success"] += 1
                total_success += 1
            total_challenges += 1
            
    # Calculate achievement rate
    achievement_rate = (total_success / total_challenges * 100) if total_challenges > 0 else 0.0
    
    # Convert map to sorted list
    daily_stats_list = []
    for i in range(7):
        day_key = start_of_week + timedelta(days=i)
        stats = daily_stats_map[day_key]
        daily_stats_list.append(DailyStat(
            date=stats["date"],
            total=stats["total"],
            success=stats["success"]
        ))
        
    return ChallengeWeeklyStatsResponse(
        total_challenges=total_challenges,
        achievement_rate=round(achievement_rate, 1),
        daily_stats=daily_stats_list
    )