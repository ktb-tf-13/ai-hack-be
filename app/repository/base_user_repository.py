from abc import ABC, abstractmethod
from app.model.models import User

class BaseUserRepository(ABC):
    @abstractmethod
    async def insert_user(self, user: User):
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: str) -> User:
        pass
