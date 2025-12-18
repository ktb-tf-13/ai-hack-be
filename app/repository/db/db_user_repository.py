from sqlalchemy.ext.asyncio import AsyncSession
import logging
import app.model.models as models
from app.repository.base_user_repository import BaseUserRepository

logger = logging.getLogger(__name__)

class UserRepositoryDB(BaseUserRepository):
    def __init__(self, db: AsyncSession):
        super().__init__()
        self.db = db

    async def insert_user(self, user: models.User) :
        self.db.add(user) # add는 await 없음
        await self.db.commit() # commit은 await 필수
        await self.db.refresh(user) # refresh는 await 필수