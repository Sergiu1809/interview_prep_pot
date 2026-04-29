from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.users import User
from app.models.sessions import Session as SessionModel
from app.models.questions import Question
from app.models.answers import Answer
from app.schemas.session import SessionCreate, SessionResponse
from app.schemas.question import QuestionRequest, QuestionResponse
from app.schemas.answer import AnswerRequest, AnswerResponse
from app.services.ai_service import generate_question, evaluate_answer
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

    try:
        question_text = generate_question(
            session.topic, question_data.difficulty, question_number)
    except Exception:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="AI evaluation service is currently unavailable")

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


@router.post("/{session_id}/{question_id}/answer", response_model=AnswerResponse, status_code=status.HTTP_201_CREATED)
def answer_submission(session_id: int, question_id: int,
                      answer_data: AnswerRequest,
                      db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)
                      ):

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

    question = db.query(Question).filter(Question.id == question_id).first()

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")

    if question.session_id != session.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Question does not belong to this session")

    existing_answer = db.query(Answer).filter(
        Answer.question_id == question.id).first()
    if existing_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This question has already been answered")

    try:
        evaluate = evaluate_answer(
            question.question_text, answer_data.answer_text)
    except Exception:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="AI evaluation service is currently unavailable")

    new_answer = Answer(
        answer_text=answer_data.answer_text,
        feedback=evaluate["feedback"],
        score=evaluate["score"],
        model_answer=evaluate["model_answer"],
        question_id=question.id
    )

    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)

    return new_answer
