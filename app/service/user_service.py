import app.schema.user_schema as user_schema
import app.model.models as app_models
import app.core.security as security
from app.repository.base_user_repository import BaseUserRepository
import logging
from app.core.exception import CustomException, ErrorCode

logger = logging.getLogger(__name__)

async def create_user(repo:BaseUserRepository, data:user_schema.UserCreate) :

    hashedPassword = security.get_password_hash(data.password)
    user = app_models.User(
        user_id=data.user_id,
        password=hashedPassword,
        nickname=data.nickname,
        img_id=data.img_id
    )
    try :
        await repo.insert_user(user)
    except Exception as e:
        logger.error("error", exc_info=True)
        raise CustomException(code=ErrorCode.INVALID_INPUT_VALUE, message="회원가입에 실패하였습니다.")



async def get_user_answer_status(repo: BaseUserRepository, user_id: str) -> bool:
    user = await repo.get_user_by_id(user_id)
    if not user:
        # 유저가 없으면 아직 답변하지 않은 것으로 간주하거나 에러 처리. 
        # 여기서는 False 반환
        return False
    return user.is_answered


async def get_user_goal(repo: BaseUserRepository, user_id: str) -> str | None:
    user = await repo.get_user_by_id(user_id)
    if not user:
        raise CustomException(code=ErrorCode.USER_NOT_FOUND, message="사용자를 찾을 수 없습니다.")
    return user.goal_content

