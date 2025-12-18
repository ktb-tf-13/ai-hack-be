from sqlalchemy import Column, Integer, String, Text, DateTime, BigInteger, ForeignKey, Boolean, Date
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    pass

# --- User 테이블 ---
class User(Base):
    __tablename__ = "User"
    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    password = Column(String(255), nullable=False)
    nickname = Column(String(100), nullable=False) # UNIQUE 제약조건 제거
    img_id = Column(String(50)) # 외래키 정보 제거

#-- Record 테이블 -- 
class Record(Base):
    __tablename__ = "Record"

    record_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("User.user_id", ondelete="CASCADE"), nullable=False)
    record_content = Column(String(255), nullable=True)
    # SQL에서 is_written으로 바꿨는지, is_wrote인지 확인 필요 (아까 is_written으로 하기로 함)
    record_is_written = Column(Boolean, default=False, nullable=False)
    record_date = Column(Date, nullable=False)
