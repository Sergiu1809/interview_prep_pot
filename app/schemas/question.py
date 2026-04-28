from pydantic import BaseModel
from datetime import datetime
from typing import Literal


class QuestionRequest(BaseModel):
    difficulty: Literal["easy", "medium", "hard"] = "easy"


class QuestionResponse(BaseModel):
    id: int
    question_number: int
    question_text: str
    difficulty: str
    timestamp: datetime
    session_id: int

    class Config:
        from_attributes = True
