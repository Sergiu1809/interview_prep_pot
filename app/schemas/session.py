from pydantic import BaseModel, ConfigDict
from datetime import datetime


class SessionCreate(BaseModel):
    topic: str


class SessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    topic: str
    status: str
    user_id: int
    timestamp: datetime
