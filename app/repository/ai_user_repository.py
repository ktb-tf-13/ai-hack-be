from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.model.models import User

class AIUserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(self, user_id: str):
        # user_id is String
        result = await self.db.execute(select(User).where(User.user_id == user_id))
        return result.scalars().first()

    async def create_user_if_not_exists(self, user_id: str) -> User:
        user = await self.get_user_by_id(user_id)
        if not user:
            try:
                # user_id 지정 생성 (String)
                new_user = User(user_id=user_id, user_name=f"User_{user_id}", is_answered=False)
                self.db.add(new_user)
                await self.db.commit()
                await self.db.refresh(new_user)
                return new_user
            except Exception:
                await self.db.rollback()
                return await self.get_user_by_id(user_id)
        return user

    async def update_user_goal(self, user_id: str, goal_content: str):
        user = await self.get_user_by_id(user_id)
        if user:
            user.goal_content = goal_content
            user.is_answered = True
            await self.db.commit()
            await self.db.refresh(user)
            return user
        return None
