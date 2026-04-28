from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.users import User
from app.models.sessions import Session as SessionModel
from app.models.questions import Question
from app.schemas.session import SessionCreate, SessionResponse
from app.schemas.question import QuestionRequest, QuestionResponse
from app.services.ai_service import generate_question
from app.dependencies import get_current_user


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


@router.post("/{session_id}/next-question", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
def create_question(session_id: int,
                    question_data: QuestionRequest,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):

    session = db.query(SessionModel).filter(
        SessionModel.id == session_id).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    if session.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to access this session")

    if session.status != "active":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Session is no longer active")

    question_number = db.query(Question).filter(
        Question.session_id == session_id).count() + 1

    question_text = generate_question(
        session.topic, question_data.difficulty, question_number)

    new_question = Question(
        question_number=question_number,
        question_text=question_text,
        difficulty=question_data.difficulty,
        session_id=session.id
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return new_question
# test
