from pydantic import BaseModel
from datetime import datetime


class SessionCreate(BaseModel):
    topic: str


class SessionResponse(BaseModel):
    id: int
    topic: str
    status: str
    user_id: int
    timestamp: datetime

    class Config:
        from_attributes = True
