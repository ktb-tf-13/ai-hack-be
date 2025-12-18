from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from app.model.models import Challenge
from typing import List
from datetime import date

class ChallengeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_challenges_by_date(self, user_id: int, target_date: date) -> List[Challenge]:
        result = await self.db.execute(
            select(Challenge)
            .where(Challenge.user_id == user_id)
            .where(Challenge.challenge_date == target_date)
        )
        return result.scalars().all()

    async def get_challenges_by_period(self, user_id: int, start_date: date, end_date: date) -> List[Challenge]:
        result = await self.db.execute(
            select(Challenge)
            .where(Challenge.user_id == user_id)
            .where(Challenge.challenge_date >= start_date)
            .where(Challenge.challenge_date <= end_date)
        )
        return result.scalars().all()

    async def delete_challenges_by_date(self, user_id: int, target_date: date):
        await self.db.execute(
            delete(Challenge)
            .where(Challenge.user_id == user_id)
            .where(Challenge.challenge_date == target_date)
        )
        await self.db.commit()

    async def create_challenge(self, user_id: int, content: str, date: date):
        challenge = Challenge(
            user_id=user_id,
            challenge_content=content,
            challenge_date=date,
            challenge_is_checked=False
        )
        self.db.add(challenge)
        return challenge  # commit은 외부에서 일괄 처리 권장하지만 여기서는 편의상 서비스에서 처리

    async def get_recent_challenges(self, user_id: int, limit: int = 5) -> List[Challenge]:
        result = await self.db.execute(
            select(Challenge)
            .where(Challenge.user_id == user_id)
            .order_by(Challenge.challenge_date.desc())
            .limit(limit)
        )
        # 시간 역순으로 가져왔으니 다시 시간순으로 정렬해서 반환하거나 그대로 사용
        return result.scalars().all()

    async def commit(self):
        await self.db.commit()
