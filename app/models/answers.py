from sqlalchemy import Integer, Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    answer_text = Column(String, nullable=False)
    feedback = Column(String, nullable=True)
    score = Column(Integer, nullable=True)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(
        timezone.utc), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    question = relationship("Question", back_populates="answer")
