from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.model.models import User

class AIUserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(self, user_id: int):
        # user_id is BIGINT
        result = await self.db.execute(select(User).where(User.user_id == user_id))
        return result.scalars().first()

    async def create_user_if_not_exists(self, user_id: int) -> User:
        user = await self.get_user_by_id(user_id)
        if not user:
            # user_id는 AUTO_INCREMENT라서 보통은 입력받지 않지만, 
            # 여기서는 클라이언트가 보넨 ID로 강제 생성하거나(주의), 
            # 혹은 user_id=0 같은 임시 ID라면 새로 생성해서 그 ID를 반환해야 함.
            # 하지만 요구사항은 "유저를 생성해줘"이므로, 
            # 만약 user_id가 요청에 포함되어 있다면 그 ID를 가진 유저가 있어야 함.
            # AUTO_INCREMENT라서 특정 ID로 INSERT하려면 IDENTITY_INSERT 등의 설정이 필요할 수 있음.
            # 여기서는 편의상 user_id를 지정하지 않고 생성한 뒤, 그 생성된 유저를 사용하도록 하거나
            # MySQL에서 user_id를 명시적으로 넣는 것을 시도함.
            try:
                # user_id를 직접 지정해서 생성 시도 (MySQL 기본 설정상 가능할 수 있음)
                new_user = User(user_id=user_id, user_name=f"User_{user_id}", is_answered=False)
                self.db.add(new_user)
                await self.db.commit()
                await self.db.refresh(new_user)
                return new_user
            except Exception:
                await self.db.rollback()
                # 이미 존재하거나 다른 이슈라면 다시 조회
                return await self.get_user_by_id(user_id)
        return user

    async def update_user_goal(self, user_id: int, goal_content: str):
        user = await self.get_user_by_id(user_id)
        if user:
            user.goal_content = goal_content
            user.is_answered = True
            await self.db.commit()
            await self.db.refresh(user)
            return user
        return None
