from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.sessions import Session as SessionModel
from app.schemas.session import SessionCreate, SessionResponse
from app.dependencies import get_current_user
from app.models.users import User

router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.post("/", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(session_data: SessionCreate,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    new_session = SessionModel(
        topic=session_data.topic,
        user_id=current_user.id
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session
