
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Date, ForeignKey, JSON, BigInteger
from sqlalchemy.orm import DeclarativeBase, relationship

from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "User"
    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_name = Column(String(255), nullable=True)
    is_answered = Column(Boolean, default=False, nullable=False)
    goal_content = Column(Text, nullable=True)

class Challenge(Base):
    __tablename__ = "Challenge"
    challenge_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("User.user_id", ondelete="CASCADE"), nullable=False)
    challenge_content = Column(String(255), nullable=False)
    challenge_is_checked = Column(Boolean, default=False, nullable=False)
    challenge_date = Column(Date, nullable=False)

class Record(Base):
    __tablename__ = "Record"
    record_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("User.user_id", ondelete="CASCADE"), nullable=False)
    record_content = Column(String(255), nullable=True)
    record_is_wrote = Column(Boolean, default=False, nullable=False)
    record_date = Column(Date, nullable=False)

class WeeklyReport(Base):
    __tablename__ = "WeeklyReport"
    report_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("User.user_id", ondelete="CASCADE"), nullable=False)
    year = Column(Integer, nullable=False)
    week = Column(Integer, nullable=False)
    summary = Column(Text, nullable=False)
    feedback = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

class OnboardingSession(Base):
    __tablename__ = "OnboardingSession"
    session_id = Column(String(36), primary_key=True)
    user_id = Column(BigInteger, ForeignKey("User.user_id", ondelete="SET NULL"), nullable=True)
    current_step = Column(Integer, default=0)
    history_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
