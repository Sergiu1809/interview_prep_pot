from fastapi import HTTPException, status
from app.models.users import User
from app.models.sessions import Session as SessionModel
from sqlalchemy.orm import Session


def get_session_or_raise(session_id: int, current_user: User, db: Session) -> SessionModel:

    session = db.query(SessionModel).filter(
        SessionModel.id == session_id).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    if session.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to access this session")

    return session
