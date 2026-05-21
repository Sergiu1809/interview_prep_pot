from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class SessionCreate(BaseModel):
    topic: str = Field(min_length=1, max_length=50)


class SessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    topic: str
    status: str
    user_id: int
    timestamp: datetime
