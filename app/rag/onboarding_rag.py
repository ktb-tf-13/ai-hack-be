from typing import List, Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.rag.base import llm_client
from app.rag.prompts import SYSTEM_PROMPT_ONBOARDING_QUESTION, SYSTEM_PROMPT_ONBOARDING_CHALLENGE

# JSON 파서 설정
json_parser = JsonOutputParser()

# 프롬프트 템플릿 설정
question_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT_ONBOARDING_QUESTION),
    ("user", "대화 기록: {history}\n\n위 대화 맥락을 바탕으로 다음 질문을 생성해줘.")
])

challenge_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT_ONBOARDING_CHALLENGE),
    ("user", "대화 기록: {history}\n최종 목표: {final_goal}\n\n위 내용을 분석하여 맞춤형 챌린지를 생성해줘.")
])

async def generate_next_question(history: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    온보딩용 다음 질문 생성 (LangChain Chain 사용)
    """
    llm = llm_client.get_llm()
    if not llm:
        return {"question": "API Key Missing", "options": ["확인"]}

    # Chain 구성: Prompt -> LLM -> JSON Parser
    chain = question_prompt | llm | json_parser
    
    # history 리스트를 문자열로 변환하여 주입
    history_str = "\n".join([f"{item['role']}: {item['content']}" for item in history])
    
    try:
        return await chain.ainvoke({"history": history_str})
    except Exception as e:
        print(f"❌ RAG Error: {e}")
        return {"question": "질문 생성 실패", "options": ["다시 시도"]}

async def generate_final_challenge(history: List[Dict[str, str]], final_goal: str) -> Dict[str, Any]:
    """
    온보딩 완료 후 최종 챌린지 생성 (LangChain Chain 사용)
    """
    llm = llm_client.get_llm()
    if not llm:
        return {"challenge_title": "API Key Missing"}

    chain = challenge_prompt | llm | json_parser
    
    history_str = "\n".join([f"{item['role']}: {item['content']}" for item in history])

    try:
        return await chain.ainvoke({"history": history_str, "final_goal": final_goal})
    except Exception as e:
        print(f"❌ RAG Error: {e}")
        return {"challenge_title": "생성 실패"}
