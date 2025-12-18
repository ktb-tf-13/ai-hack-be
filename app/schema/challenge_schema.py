from pydantic import BaseModel
from typing import List

# 요청 받을 데이터 (Body)
class ChallengeRequest(BaseModel):
    user_id: str
    date: str

class ChallengeCompleteRequest(BaseModel):
    user_id: str
    id: str
    date: str

class ChallengeCancelRequest(BaseModel):
    user_id: str
    id: str
    date: str

class ChallengeDeleteRequest(BaseModel):
    id: int

class ChallengeWeeklyStatsRequest(BaseModel):
    user_id: str
    date: str # "YYYYMMDD"

class DailyStat(BaseModel):
    date: str # "12.15(월)"
    total: int
    success: int

class ChallengeWeeklyStatsResponse(BaseModel):
    total_challenges: int
    achievement_rate: float
    daily_stats: List[DailyStat]