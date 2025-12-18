from app.schema.ai_schema import (
    AIChallengeGenerateRequest, 
    AIChallengeGenerateResponse,
    AIWeeklyReportRequest,
    AIWeeklyReportResponse, 
    OnboardingRequest, 
    OnboardingResponse, 
    OnboardingStepType
)

from app.repository.onboarding_repository import OnboardingRepository
from app.repository.ai_user_repository import AIUserRepository
from app.repository.challenge_repository import ChallengeRepository
from app.repository.report_repository import ReportRepository
from app.repository.record_repository import RecordRepository

from app.rag import challenge_rag, onboarding_rag, report_rag
import uuid
from typing import Dict, List

from datetime import date, timedelta, datetime
from sqlalchemy.ext.asyncio import AsyncSession

async def generate_weekly_report(request: AIWeeklyReportRequest, db: AsyncSession) -> AIWeeklyReportResponse:
    challenge_repo = ChallengeRepository(db)
    report_repo = ReportRepository(db)

    try:
        user_id_int = int(request.user_id)
    except ValueError:
        return AIWeeklyReportResponse(success=False, message="유저 ID는 숫자여야 합니다.", summary=None)

    # 날짜 파싱 및 주차 계산
    try:
        # YYYYMMDD -> date 객체
        target_dt = datetime.strptime(request.target_date, "%Y%m%d").date()
        year, week, weekday = target_dt.isocalendar()
    except ValueError:
        return AIWeeklyReportResponse(success=False, message="날짜 형식이 올바르지 않습니다. (YYYYMMDD)", summary=None)

    # 1. 기존 리포트 존재 확인
    existing_report = await report_repo.get_weekly_report(user_id_int, year, week)
    if existing_report:
        return AIWeeklyReportResponse(
            success=True,
            message="이미 주간 리포트가 존재합니다.",
            summary=existing_report.summary,
            feedback=existing_report.feedback
        )

    # 2. 날짜 계산
    try:
        start_date = date.fromisocalendar(year, week, 1)
        end_date = date.fromisocalendar(year, week, 7)
    except ValueError:
        return AIWeeklyReportResponse(success=False, message="날짜 계산 오류", summary=None)

    # 2. 챌린지 조회
    challenges = await challenge_repo.get_challenges_by_period(user_id_int, start_date, end_date)
    
    # RAG용 데이터 변환
    challenges_data = []
    for ch in challenges:
        challenges_data.append({
            "date": str(ch.challenge_date),
            "content": ch.challenge_content,
            "is_completed": ch.challenge_is_checked
        })

    # 3. RAG 호출
    result = await report_rag.generate_weekly_report(year, week, challenges_data)
    summary = result.get("summary", "")
    feedback = result.get("feedback", "")

    # 4. DB 저장
    await report_repo.create_weekly_report(user_id_int, year, week, summary, feedback)
    print(f"📖 주간 리포트 저장 완료 ({year}-{week})")

    return AIWeeklyReportResponse(
        success=True,
        message="주간 리포트가 생성되었습니다.",
        summary=summary,
        feedback=feedback
    )

async def process_onboarding(request: OnboardingRequest, db: AsyncSession) -> OnboardingResponse:
    
    INITIAL_QUESTION = {
    "question": "요즘 가장 해결하고 싶은 고민이나 이루고 싶은 목표는 무엇인가요?",
    "options": ["건강/운동", "자기계발/학습", "마음챙김/휴식", "취업/이직", "자산관리"]
    }
    
    repo = OnboardingRepository(db)
    user_repo = AIUserRepository(db)

    # 0. 유저 존재 확인 및 생성
    if request.user_id:
        await user_repo.create_user_if_not_exists(request.user_id)
    
    # 1. 세션 ID 생성/조회
    session_id = request.session_id if request.session_id else str(uuid.uuid4())
    session = await repo.get_session(session_id)
    
    

    if not session:
        session = await repo.create_session(session_id, request.user_id)
        history = []
    else:
        # DB에서 가져온 JSON (List[Dict])
        history = session.history_data if session.history_data else []

    # 2. 현재 스텝 및 답변 처리
    current_answered_step = request.step if request.step else 1
    next_step = current_answered_step + 1

    if request.answer:
        history.append({"role": "answer", "content": request.answer})
    
    # 3. 단계별 로직
    if next_step <= 10:
        if current_answered_step == 1 and not request.answer: 
             # 첫 진입 (답변 없음, 스텝 1이라고 가정하지만 실제 로직에 따라 다를 수 있음)
             # 여기서는 단순화: answer가 없으면 첫 질문 리턴
            generated = INITIAL_QUESTION
        elif current_answered_step == 1:
            generated = await onboarding_rag.generate_next_question(history)
        else:
            generated = await onboarding_rag.generate_next_question(history)
            
        history.append({"role": "question", "content": generated["question"]})
        
        # DB 업데이트
        await repo.update_history(session_id, history, next_step)

        return OnboardingResponse(
            type=OnboardingStepType.QUESTION,
            session_id=session_id,
            next_step=next_step,
            content=generated["question"],
            options=generated["options"]
        )
    
    elif next_step == 11:
        await repo.update_history(session_id, history, next_step)
        return OnboardingResponse(
            type=OnboardingStepType.GOAL_INPUT,
            session_id=session_id,
            next_step=next_step,
            content="지금까지의 답변을 바탕으로 당신의 최종 목표를 자유롭게 적어주세요."
        )

    else:
        final_goal = request.answer
        challenge_info = await onboarding_rag.generate_final_challenge(history, final_goal)
        print(f"✅ 생성된 챌린지: {challenge_info}")
        
        # 유저 목표 저장
        if request.user_id:
            # challenge_info는 Dict이므로 문자열로 변환 필요
            if isinstance(challenge_info, dict):
                # 'challenge', 'content', 'goal' 등 주요 키에서 값을 추출 시도
                goal_str = challenge_info.get("challenge") or challenge_info.get("content") or challenge_info.get("goal") or str(challenge_info)
            else:
                goal_str = str(challenge_info)
            
            # 길이 제한 고려 제거 (이제 TEXT 타입)
            await user_repo.update_user_goal(request.user_id, goal_str)
        
        await repo.update_history(session_id, history, next_step)

        return OnboardingResponse(
            type=OnboardingStepType.COMPLETE,
            session_id=session_id,
            message=f"✅ 생성된 챌린지: {challenge_info}",
            redirect_url="/main"
        )


async def generate_daily_challenge(request: AIChallengeGenerateRequest, db: AsyncSession) -> AIChallengeGenerateResponse:
    user_repo = AIUserRepository(db)
    challenge_repo = ChallengeRepository(db)
    record_repo = RecordRepository(db)

    # user_id는 숫자형으로 변환 (스키마가 str이라면 int로 변환 필요, DB는 BIGINT)
    try:
        user_id_int = int(request.user_id)
    except ValueError:
        return AIChallengeGenerateResponse(success=False, message="유저 ID는 숫자여야 합니다.")

    today_date = datetime.today().date()

    # 1. 오늘 날짜 챌린지 확인
    existing_challenges = await challenge_repo.get_challenges_by_date(user_id_int, today_date)
    
    if existing_challenges:
        if not request.refresh:
            return AIChallengeGenerateResponse(
                success=True,
                message="오늘의 챌린지가 이미 존재합니다."
            )
        else:
            print(f"🗑️ 기존 챌린지 삭제 (User: {user_id_int}, Date: {today_date})")
            await challenge_repo.delete_challenges_by_date(user_id_int, today_date)

    # 2. 유저 정보 및 기록 조회
    user = await user_repo.get_user_by_id(user_id_int)
    if not user:
         return AIChallengeGenerateResponse(success=False, message="유저가 존재하지 않습니다.")
    
    goal = user.goal_content if user.goal_content else "목표 설정 필요"
    
    # 최근 10개 기록(Record) & 챌린지(Challenge) 조회
    recent_challenges = await challenge_repo.get_recent_challenges(user_id_int, limit=10)
    recent_records = await record_repo.get_recent_records(user_id_int, limit=10)

    # 날짜별로 데이터 정리 (Dict[date, Dict])
    history_map = {}
    
    # 챌린지 데이터 병합
    for ch in recent_challenges:
        d = ch.challenge_date
        if d not in history_map:
            history_map[d] = {"challenges": [], "record": "기록 없음"}
        
        status = "성공" if ch.challenge_is_checked else "실패"
        history_map[d]["challenges"].append(f"{ch.challenge_content}({status})")

    # 레코드 데이터 병합
    for rec in recent_records:
        d = rec.record_date
        content = rec.record_content if rec.record_is_wrote and rec.record_content else "기록 없음"
        if d not in history_map:
             history_map[d] = {"challenges": ["챌린지 없음"], "record": content}
        else:
             history_map[d]["record"] = content
    
    # 최신순 정렬 후 문자열 생성
    sorted_dates = sorted(history_map.keys(), reverse=True)[:10] # 최근 10일
    
    if not sorted_dates:
        history = "이전 활동 기록 없음 (오늘 처음 시작)"
    else:
        history_lines = []
        for d in sorted_dates:
            data = history_map[d]
            ch_str = ", ".join(data["challenges"])
            rec_str = data["record"]
            history_lines.append(f"- {d}: [챌린지] {ch_str} | [일기] {rec_str}")
        history = "\n".join(history_lines)

    # 3. RAG 호출
    result = await challenge_rag.generate_daily_challenge(goal, history)
    challenges_data = result.get("challenges", [])
    if not challenges_data:
        return AIChallengeGenerateResponse(success=False, message="챌린지 생성 실패 (AI 응답 오류)")

    # 4. DB 저장
    count = 0
    for item in challenges_data:
        content = item.get("content", "내용 없음")
        await challenge_repo.create_challenge(user_id_int, content, today_date)
        count += 1
    
    await challenge_repo.commit()
    print(f"💾 챌린지 {count}개 저장 완료")

    return AIChallengeGenerateResponse(
        success=True,
        message=f"{count}개의 챌린지가 생성되었습니다."
    )
