from pydantic import BaseModel
from datetime import date

# 요청 (Request)
class RecordRequest(BaseModel):
    user_id: int
    content: str
    date: date # "2025-12-17" 형태의 문자열을 자동으로 date 객체로 변환해줌

# 응답 (Response)
class RecordResponse(BaseModel):
    id: int
    content: str
    date: date

class RecordSearchRequest(BaseModel):
    user_id: int
    date: date