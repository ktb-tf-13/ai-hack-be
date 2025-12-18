from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
import logging
import app.model.models as models
from app.repository.base_user_repository import BaseUserRepository

logger = logging.getLogger(__name__)

class UserRepositoryDB(BaseUserRepository):
    def __init__(self, db: AsyncSession):
        super().__init__()
        self.db = db

    async def insert_user(self, user: models.User) :
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user) # DB에서 생성된 값(default 등)을 인스턴스에 반영