from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
import logging
import app.model.models as models

logger = logging.getLogger(__name__)

class ChallengeRepositoryDB:
    def __init__(self, db: Session):
        self.db = db

    # 챌린지 목록 조회
    def get_challenges(self, user_id: int, date: str):
        # SELECT * FROM Challenge WHERE user_id = ... AND challenge_date = ...
        stmt = select(models.Challenge).where(
            models.Challenge.user_id == user_id,
            models.Challenge.challenge_date == date
        )
        result = self.db.execute(stmt)
        return result.scalars().all()

    # 챌린지 상태 변경 (완료/취소 공용)
    def update_challenge_status(self, challenge_id: int, is_checked: bool):
        # UPDATE Challenge SET challenge_is_checked = ... WHERE challenge_id = ...
        stmt = update(models.Challenge).where(
            models.Challenge.challenge_id == challenge_id
        ).values(challenge_is_checked=is_checked)
        
        self.db.execute(stmt)
        self.db.commit()
        
        # 업데이트된 객체를 다시 조회해서 반환 (선택 사항)
        return {"id": challenge_id, "is_checked": is_checked}

    # 3. 챌린지 삭제
    def delete_challenge(self, challenge_id: int):
        # DELETE FROM Challenge WHERE challenge_id = ...
        stmt = delete(models.Challenge).where(
            models.Challenge.challenge_id == challenge_id
        )
        
        self.db.execute(stmt)
        self.db.commit()
        
        return {"id": challenge_id, "is_deleted": True}