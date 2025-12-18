from fastapi import APIRouter
from app.schema.challenge_schema import (
    ChallengeRequest, 
    ChallengeCompleteRequest, 
    ChallengeCancelRequest,
    ChallengeDeleteRequest
)

router = APIRouter()

@router.post("/challenges")
def get_challenges(request: ChallengeRequest):
    
    # 로직

    # 들어온 요청 값(request.user_id 등)을 로그로 확인해볼 수 있습니다.
    print(f"DEBUG: 요청 들어옴 - user_id: {request.user_id}, date: {request.date}")

    # DB 조회 로직 대신, 하드코딩된 더미 데이터 반환
    return {
        "challenges": [
            {
                "id": 1,
                "user_id": request.user_id, # 요청받은 ID를 그대로 넣어주면 더 리얼합니다
                "content": "아침 물 한 잔 마시기",
                "is_checked": False,
                "date": request.date,       # 요청받은 날짜를 그대로 반환
            },
            {
                "id": 2,
                "user_id": request.user_id,
                "content": "아침 조깅",
                "is_checked": False,
                "date": request.date,
            }
        ]
    }

# 챌린지 완료
@router.post("/users/challenges/complete")
def complete_challenge(request: ChallengeCompleteRequest):
    
    print(f"DEBUG: 챌린지 완료 요청됨 - ID: {request.id}")

    #더미데이터 반환
    return {
        "id": request.id,
        "is_checked": True
    }

# 챌린지 완료 취소
@router.post("/users/challenges/cancel")
def complete_challenge(request: ChallengeCancelRequest):
    
    print(f"DEBUG: 챌린지 실패 요청됨 - ID: {request.id}")

    #더미데이터 반환
    return {
        "id": request.id,
        "is_checked": False
    }

# 챌린지 삭제
@router.delete("/users/challenges/delete")
def delete_challenge(request: ChallengeDeleteRequest):
    
    print(f"DEBUG: 챌린지 삭제 요청됨 - ID: {request.id}")

    # 나중에 실제 DB 연결 시:
    # 1. db.query(Challenge).filter(Challenge.id == request.id).delete()
    # 2. db.commit()
    
    # 지금은 더미 데이터 반환
    return {
        "id": request.id,
        "is_deleted": True,
        "message": "챌린지가 성공적으로 삭제되었습니다."
    }