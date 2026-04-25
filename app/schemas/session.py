from pydantic import BaseModel


class Session(BaseModel):
    topic: str
