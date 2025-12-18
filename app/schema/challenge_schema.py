from pydantic import BaseModel

# 요청 받을 데이터 (Body)
class ChallengeRequest(BaseModel):
    user_id: int
    date: str

class ChallengeCompleteRequest(BaseModel):
    id: int

class ChallengeCancelRequest(BaseModel):
    id: int

class ChallengeDeleteRequest(BaseModel):
    id: int