from typing import Optional
from pydantic import BaseModel

class ProfessorBase(BaseModel):
    name: str
    email: Optional[str] = None
    ta_preferences: Optional[str] = None
    req_tas: Optional[int] = None

class ProfessorCreate(ProfessorBase):
    pass

class ProfessorRead(ProfessorBase):
    id: int

    class Config:
        orm_mode = True