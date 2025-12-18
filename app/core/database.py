from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
    print("WARNING: DB_NAME is missing. Using default 'tf13' or 'backend'.")
    # 🔥 여기에 실제 RDS에 만들어둔 DB 이름을 문자열로 적으세요!
    # 예: "backend", "mydb", "tf13" 등 
    # (로그에 USER가 tf13인 걸 보니 DB 이름도 tf13일 가능성이 높습니다)
    db_name = "tf13" 

print(f"DEBUG: HOST={settings.db_host}, PORT={settings.db_port}, USER={settings.db_user}")


# MariaDB 연결 URL
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{db_port}/{settings.db_name}"

# 연결 옵션 추가
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # 연결 유효성 체크
    pool_recycle=3600,   # 1시간마다 연결 재생성
    echo=True            # SQL 쿼리 로깅 (개발 시에만 True)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 의존성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()