from pydantic import BaseModel


class Candidate(BaseModel):
    name: str
    email: str
    phone: str
    score: float = 0.0


class JobDescription(BaseModel):
    title: str
    skills: list[str]