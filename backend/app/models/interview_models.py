from typing import Optional
from sqlmodel import SQLModel, Field


class InterviewSession(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)

    role: str
    level: str

    tech_stack: str

    question_count: int

    current_question: int = 0


class InterviewMessage(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)

    session_id: int

    sender: str

    message: str