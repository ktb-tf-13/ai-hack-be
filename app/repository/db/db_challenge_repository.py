from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
import logging
import app.model.models as models

logger = logging.getLogger(__name__)

class ChallengeRepositoryDB:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_challenges(self, user_id: int, date: str):
        stmt = select(models.Challenge).where(
            models.Challenge.user_id == user_id,
            models.Challenge.challenge_date == date
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update_challenge_status(self, challenge_id: int, is_checked: bool):
        stmt = update(models.Challenge).where(
            models.Challenge.challenge_id == challenge_id
        ).values(challenge_is_checked=is_checked)
        
        await self.db.execute(stmt)
        await self.db.commit()
        
        return {"id": challenge_id, "is_checked": is_checked}

    async def delete_challenge(self, challenge_id: int):
        stmt = delete(models.Challenge).where(
            models.Challenge.challenge_id == challenge_id
        )
        
        # [수정] 비동기 실행 및 커밋
        await self.db.execute(stmt)
        await self.db.commit()
        
        return {"id": challenge_id, "is_deleted": True}