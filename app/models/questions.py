from sqlalchemy import Integer, Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_number = Column(Integer, nullable=False)
    question_text = Column(String, nullable=False)
    difficulty = Column(String, nullable=False, default="easy")
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(
        timezone.utc), nullable=False)
    # If you pass a value to default, it's evaluated once at import time and frozen.
    # If you pass a function to default, it's called fresh every time a row is created.
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    session = relationship("Session", back_populates="questions")
    answer = relationship("Answer", back_populates="question", uselist=False)
