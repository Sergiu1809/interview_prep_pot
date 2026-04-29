from pydantic import BaseModel
from datetime import datetime


class AnswerRequest(BaseModel):
    answer_text: str


class AnswerResponse(BaseModel):
    id:  int
    answer_text: str
    feedback: str
    score: int
    model_answer: str
    timestamp: datetime
    question_id: int

    class Config:
        from_attributes = True
