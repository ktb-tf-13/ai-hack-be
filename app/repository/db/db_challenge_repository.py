from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
import logging
import app.model.models as models

logger = logging.getLogger(__name__)

class ChallengeRepositoryDB:
    def __init__(self, db: AsyncSession):
        self.db = db

    # 챌린지 목록 조회
    async def get_challenges(self, user_id: str, date: str):
        # SELECT * FROM Challenge WHERE user_id = ... AND challenge_date = ...
        stmt = select(models.Challenge).where(
            models.Challenge.user_id == user_id,
            models.Challenge.challenge_date == date
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    # 챌린지 상태 변경 (완료/취소 공용)
    async def update_challenge_status(self, challenge_id: int, user_id: str, date: str, is_checked: bool):
        # UPDATE Challenge SET challenge_is_checked = ... WHERE challenge_id = ... AND user_id = ... AND challenge_date = ...
        stmt = update(models.Challenge).where(
            models.Challenge.challenge_id == challenge_id,
            models.Challenge.user_id == user_id,
            models.Challenge.challenge_date == date
        ).values(challenge_is_checked=is_checked)
        
        await self.db.execute(stmt)
        await self.db.commit()
        
        # 업데이트된 객체를 다시 조회해서 반환 (선택 사항)
        return {"id": challenge_id, "is_checked": is_checked}

    # 3. 챌린지 삭제
    async def delete_challenge(self, challenge_id: int):
        # DELETE FROM Challenge WHERE challenge_id = ...
        stmt = delete(models.Challenge).where(
            models.Challenge.challenge_id == challenge_id
        )
        
        await self.db.execute(stmt)
        await self.db.commit()
        
        return {"id": challenge_id, "is_deleted": True}

    # 기간별 챌린지 조회
    async def get_challenges_by_period(self, user_id: str, start_date, end_date):
        stmt = select(models.Challenge).where(
            models.Challenge.user_id == user_id,
            models.Challenge.challenge_date >= start_date,
            models.Challenge.challenge_date <= end_date
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()