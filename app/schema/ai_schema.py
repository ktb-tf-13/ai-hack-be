from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

# --- Challenge Generation ---
class AIChallengeGenerateRequest(BaseModel):
    user_id: str = Field(..., description="유저 식별자 (DB 조회용)")
    refresh: bool = Field(default=False, description="강제 재생성 여부")

class AIChallengeGenerateResponse(BaseModel):
    success: bool = Field(..., description="생성 성공 여부")
    message: str = Field(..., description="결과 메시지")

# --- Weekly Report ---
class AIWeeklyReportRequest(BaseModel):
    user_id: str = Field(..., description="유저 ID")
    target_date: str = Field(..., description="기준 날짜 (YYYYMMDD, 예: 20250911)")

class AIWeeklyReportResponse(BaseModel):
    success: bool
    message: str
    summary: Optional[str] = Field(None, description="생성된 리포트 내용")
    feedback: Optional[str] = Field(None, description="부족했던 부분에 대한 피드백")

class OnboardingStepType(str, Enum):
    QUESTION = "QUESTION"
    GOAL_INPUT = "GOAL_INPUT"
    COMPLETE = "COMPLETE"

class OnboardingRequest(BaseModel):
    session_id: Optional[str] = Field(None, description="세션 ID (첫 요청 시 None)")
    user_id: str = Field(..., description="유저 ID")
    answer: Optional[str] = Field(None, description="유저 응답 (선택지 텍스트 또는 입력한 목표)")
    step: Optional[int] = Field(None, description="현재 완료한 스텝 (1~10: 질문, 11: 목표입력)")

class OnboardingResponse(BaseModel):
    type: OnboardingStepType = Field(..., description="응답 타입 (QUESTION, GOAL_INPUT, COMPLETE)")
    session_id: str = Field(..., description="세션 ID")
    next_step: Optional[int] = Field(None, description="다음 진행할 스텝 번호")
    content: Optional[str] = Field(None, description="질문 내용 또는 안내 문구")
    options: Optional[List[str]] = Field(None, description="선택지 리스트 (QUESTION 타입일 때)")
    message: Optional[str] = Field(None, description="완료 메시지 (COMPLETE 타입일 때)")
    redirect_url: Optional[str] = Field(None, description="리다이렉트 URL (COMPLETE 타입일 때)")
