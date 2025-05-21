from typing import Optional
from pydantic import BaseModel

class ProfessorBase(BaseModel):
    name: str
    email: Optional[str] = None
    ta_preferences: Optional[str] = None

class ProfessorCreate(ProfessorBase):
    pass

class ProfessorRead(ProfessorBase):
    id: int

    class Config:
        orm_mode = True