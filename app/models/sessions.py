from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, nullable=False)
    status = Column(String, default="active")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="sessions")
    questions = relationship("Question", back_populates="session")
