import asyncio
from typing import Dict, Any, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.rag.base import llm_client
from app.rag.prompts import SYSTEM_PROMPT_WEEKLY_REPORT, SYSTEM_PROMPT_WEEKLY_FEEDBACK

# JSON 파서
json_parser = JsonOutputParser()

# 프롬프트
summary_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT_WEEKLY_REPORT),
    ("user", "기간: {year}년 {week}주차\n\n[챌린지 수행 기록]\n{challenge_history}\n\n위 기록을 바탕으로 주간 주요 변화 리포트를 작성해줘.")
])

feedback_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT_WEEKLY_FEEDBACK),
    ("user", "기간: {year}년 {week}주차\n\n[챌린지 수행 기록]\n{challenge_history}\n\n위 기록을 바탕으로 부족했던 부분에 대한 피드백을 작성해줘.")
])

async def generate_weekly_report(year: int, week: int, challenges: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    주간 리포트 생성 (Summary + Feedback)
    """
    llm = llm_client.get_llm()
    if not llm:
        return {"summary": "API Key Missing", "feedback": "API Key Missing"}

    # 챌린지 기록 텍스트 변환
    history_lines = []
    if not challenges:
        history_lines.append("수행한 챌린지 기록이 없습니다.")
    else:
        for ch in challenges:
            status = "성공" if ch.get("is_completed") else "실패"
            history_lines.append(f"- {ch.get('date')} : {ch.get('content')} ({status})")
    
    challenge_history_str = "\n".join(history_lines)

    # 두 개의 체인 준비
    summary_chain = summary_prompt | llm | json_parser
    feedback_chain = feedback_prompt | llm | json_parser
    
    input_data = {
        "year": year,
        "week": week,
        "challenge_history": challenge_history_str
    }

    try:
        # 병렬 실행으로 응답 속도 향상
        summary_res, feedback_res = await asyncio.gather(
            summary_chain.ainvoke(input_data),
            feedback_chain.ainvoke(input_data)
        )
        
        return {
            "summary": summary_res.get("summary", ""),
            "feedback": feedback_res.get("feedback", "")
        }
    except Exception as e:
        print(f"❌ Report Generation Error: {e}")
        return {"summary": "생성 오류", "feedback": "생성 오류"}
