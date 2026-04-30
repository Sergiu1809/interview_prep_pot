from pydantic import BaseModel, ConfigDict
from datetime import datetime


class AnswerRequest(BaseModel):
    answer_text: str


class AnswerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:  int
    answer_text: str
    feedback: str
    score: int
    model_answer: str
    timestamp: datetime
    question_id: int
