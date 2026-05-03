from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_user
from app.models.users import User
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.database import get_db
from app.schemas.history import QuestionWithAnswer, SessionDetail, SessionSummary
from app.models.sessions import Session as SessionModel
from app.models.questions import Question
from app.models.answers import Answer
from app.services.session_service import get_session_or_raise

router = APIRouter(prefix="/sessions/history", tags=["history"])


@router.get("/", response_model=list[SessionSummary])
def get_sessions(db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):

    sessions = db.query(SessionModel).filter(
        SessionModel.user_id == current_user.id).all()

    session_summary_list = []

    for session in sessions:

        total_questions = db.query(func.count(Question.id)).filter(
            Question.session_id == session.id).scalar()

        average_score = db.query(func.avg(Answer.score)).join(
            Question).filter(Question.session_id == session.id).scalar()

        session_summary = SessionSummary(
            id=session.id,
            topic=session.topic,
            status=session.status,
            timestamp=session.timestamp,
            total_questions=total_questions,
            average_score=round(average_score, 1) if average_score else 0.0
        )

        session_summary_list.append(session_summary)

    return session_summary_list


@router.get("/{session_id}", response_model=SessionDetail)
def get_session_detail(session_id: int,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):

    session = get_session_or_raise(session_id, current_user, db)

    questions = db.query(Question).options(
        joinedload(Question.answer)).filter(
            Question.session_id == session_id
    ).all()

    session_detail = SessionDetail(
        id=session.id,
        topic=session.topic,
        status=session.status,
        timestamp=session.timestamp,
        questions=questions
    )

    return session_detail
