from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.config import settings

try:
    # 값이 있으면 정수로 변환 시도
    if settings.db_port:
        db_port = int(settings.db_port)
    else:
        # 값이 비어있으면('') 강제로 에러를 내서 except로 보냄
        raise ValueError 
except (ValueError, TypeError):
    print(f"⚠️ Invalid or missing DB_PORT: '{settings.db_port}'. Defaulting to 3306.")
    db_port = 3306

db_name = settings.db_name
if not db_name:
    print("WARNING: DB_NAME is missing. Using default 'tf13'")
    db_name = "tf13" 

print(f"DEBUG: HOST={settings.db_host}, PORT={settings.db_port}, USER={settings.db_user}, DB={db_name}")


# MariaDB 연결 URL
SQLALCHEMY_DATABASE_URL = f"mysql+aiomysql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{db_port}/{db_name}"

# 비동기 엔진 생성
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # 연결 유효성 체크
    pool_recycle=3600,   # 1시간마다 연결 재생성
    echo=True            # SQL 쿼리 로깅
)

# 비동기 세션 생성기
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False # 비동기 환경에서 필수
)

Base = declarative_base()

# 의존성 함수 (비동기 제너레이터)
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()