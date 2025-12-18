from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.model.models import OnboardingSession
from typing import Optional, Dict, Any, List
import json

class OnboardingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_session(self, session_id: str) -> Optional[OnboardingSession]:
        result = await self.db.execute(select(OnboardingSession).where(OnboardingSession.session_id == session_id))
        return result.scalars().first()

    async def create_session(self, session_id: str, user_id: Optional[str] = None) -> OnboardingSession:
        new_session = OnboardingSession(
            session_id=session_id,
            user_id=user_id,
            history_data=[]
        )
        self.db.add(new_session)
        await self.db.commit()
        await self.db.refresh(new_session)
        return new_session

    async def update_history(self, session_id: str, history: List[Dict[str, str]], current_step: int):
        session = await self.get_session(session_id)
        if session:
            # SQLAlchemy JSON 타입은 List/Dict 그대로 저장 가능하지만, 
            # 확실하게 변경 감지를 위해 새 객체 할당 추천
            session.history_data = list(history)
            session.current_step = current_step
            await self.db.commit()
            await self.db.refresh(session)
