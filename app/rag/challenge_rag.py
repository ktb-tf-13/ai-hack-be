from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.rag.base import llm_client
from app.rag.prompts import SYSTEM_PROMPT_DAILY_CHALLENGE

# JSON 파서
json_parser = JsonOutputParser()

# 프롬프트 템플릿
daily_challenge_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT_DAILY_CHALLENGE),
    ("user", "사용자 정보:\n- 최종 목표: {goal}\n- 최근 기록: {history}\n\n오늘의 챌린지를 생성해줘.")
])

async def generate_daily_challenge(goal: str, history: str) -> Dict[str, Any]:
    """
    RAG를 사용하여 오늘의 챌린지를 생성합니다.
    """
    llm = llm_client.get_llm()
    if not llm:
        return {"title": "API Key Missing", "content": "OpenAI 키를 확인해주세요."}

    chain = daily_challenge_prompt | llm | json_parser
    
    try:
        # 비동기 호출 (ainvoke)
        return await chain.ainvoke({
            "goal": goal,
            "history": history
        })
    except Exception as e:
        print(f"❌ Challenge Generation Error: {e}")
        return {
            "title": "챌린지 생성 실패",
            "content": "일시적인 오류로 챌린지를 생성하지 못했습니다. 다시 시도해주세요.",
            "category": "Error",
            "difficulty": "-",
            "reason": str(e)
        }
