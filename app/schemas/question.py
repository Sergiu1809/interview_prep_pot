from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Literal


class QuestionRequest(BaseModel):
    difficulty: Literal["easy", "medium", "hard"] = "easy"


class QuestionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question_number: int
    question_text: str
    difficulty: str
    timestamp: datetime
    session_id: int
