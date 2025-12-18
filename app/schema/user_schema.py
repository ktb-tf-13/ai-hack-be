from pydantic import BaseModel, field_validator


#1. Payload 1: 회원 가입 (모든 정보 포함)
# user_id, password, nickname, img_id
class UserCreate(BaseModel):
    user_id: str
    password: str
    nickname: str
    img_id: str

    @field_validator('user_id')
    @classmethod
    def convert_user_id_to_str(cls, v):
        return str(v)

class UserAnswerStatusResponse(BaseModel):
    is_answered: bool

class UserGoalResponse(BaseModel):
    goal: str | None