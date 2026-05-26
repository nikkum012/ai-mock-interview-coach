from fastapi import FastAPI

from fastapi import Depends

from sqlmodel import Session

from backend.app.database.db import get_session

from backend.app.models.interview_models import (
    InterviewSession,
    InterviewMessage
)



from contextlib import asynccontextmanager

from backend.app.database.db import create_db_and_tables

from backend.app.schemas.interview import InterviewConfig
from backend.app.services.interview_engine import InterviewEngine

@asynccontextmanager
async def lifespan(app: FastAPI):

    create_db_and_tables()

    yield

app = FastAPI(lifespan=lifespan)

sessions = {}

@app.get("/")
def root():
    return {"message": "AI Mock Interview Coach API"}

@app.post("/start-interview")
def start_interview(
    config: InterviewConfig,
    db: Session = Depends(get_session)
):

    session = InterviewSession(
        role=config.role,
        level=config.level,
        tech_stack=",".join(config.tech_stack),
        question_count=config.question_count
    )

    db.add(session)

    db.commit()

    db.refresh(session)

    engine = InterviewEngine(config)

    first_question = engine.generate_question()

    message = InterviewMessage(
    session_id=session.id,
    sender="ai",
    message=first_question
)

    db.add(message)

    db.commit()

    return {
        "session_id": session.id,
        "first_question": first_question
    }

@app.get("/next-question")
def next_question():

    engine = sessions["session_1"]

    question = engine.generate_question()

    return {
        "question": question,
        "question_number": engine.current_question
    }


@app.post("/session/{session_id}/message")
def send_message(
    session_id: int,
    user_message: str,
    db: Session = Depends(get_session)
):

    user_msg = InterviewMessage(
        session_id=session_id,
        sender="user",
        message=user_message
    )

    db.add(user_msg)

    response = f"Received: {user_message}"

    ai_msg = InterviewMessage(
        session_id=session_id,
        sender="ai",
        message=response
    )

    db.add(ai_msg)

    db.commit()

    return {
        "response": response
    }


@app.get("/sessions")
def get_sessions(
    db: Session = Depends(get_session)
):

    sessions = db.query(InterviewSession).all()

    return sessions


@app.get("/session/{session_id}")
def get_session_messages(
    session_id: int,
    db: Session = Depends(get_session)
):

    messages = db.query(InterviewMessage).filter(
        InterviewMessage.session_id == session_id
    ).all()

    return messages