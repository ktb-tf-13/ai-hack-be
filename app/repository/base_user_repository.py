from abc import ABC, abstractmethod
from app.model.models import User

class BaseUserRepository(ABC):
    @abstractmethod
    async def insert_user(self, user: User):
        pass
