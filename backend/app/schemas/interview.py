from pydantic import BaseModel

class InterviewConfig(BaseModel):
    role: str
    level: str
    tech_stack: list[str]
    question_count: int