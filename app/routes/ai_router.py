from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema.ai_schema import (
    AIChallengeGenerateRequest, 
    AIChallengeGenerateResponse,
    AIWeeklyReportRequest,
    AIWeeklyReportResponse,
    OnboardingRequest, 
    OnboardingResponse
)
import app.service.ai_service as ai_service
from app.core.database import get_db

router = APIRouter(prefix="/ai", tags=["AI 기능"])

@router.post("/reports/weekly", response_model=AIWeeklyReportResponse)
async def create_weekly_report(request: AIWeeklyReportRequest, db: AsyncSession = Depends(get_db)):
    """
    주간 회고 리포트 생성 (RAG)
    """
    return await ai_service.generate_weekly_report(request, db)

@router.post("/onboarding/step", response_model=OnboardingResponse)
async def onboarding_step(request: OnboardingRequest, db: AsyncSession = Depends(get_db)):
    """
    RAG 기반 온보딩 (질문 생성 -> 답변 -> ... -> 목표 설정)
    """
    return await ai_service.process_onboarding(request, db)

@router.post("/challenges", response_model=AIChallengeGenerateResponse)
async def create_daily_challenge(request: AIChallengeGenerateRequest, db: AsyncSession = Depends(get_db)):
    """
    RAG 기반 오늘의 챌린지 생성
    """
    return await ai_service.generate_daily_challenge(request, db)
