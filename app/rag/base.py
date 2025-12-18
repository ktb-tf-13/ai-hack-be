from langchain_openai import ChatOpenAI
from app.config import settings

class LLMClient:
    def __init__(self):
        try:
            self.llm = ChatOpenAI(
                api_key=settings.openai_api_key,
                model="gpt-4o",
                temperature=0.7
            )
        except Exception:
            self.llm = None
            print("⚠️ OpenAI API Key가 설정되지 않았습니다. RAG 기능이 작동하지 않을 수 있습니다.")

    def get_llm(self):
        return self.llm

# 싱글톤 인스턴스
llm_client = LLMClient()
