from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.schemas.answer import AnswerResponse


class QuestionWithAnswer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question_number: int
    question_text: str
    difficulty: str
    answer: Optional[AnswerResponse] = None  # could be null if unanswered


class SessionDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    topic: str
    status: str
    timestamp: datetime
    questions: list[QuestionWithAnswer] = []


class SessionSummary(BaseModel):
    id: int
    topic: str
    status: str
    timestamp: datetime
    total_questions: int
    average_score: float
