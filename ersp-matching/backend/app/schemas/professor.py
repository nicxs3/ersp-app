from pydantic import BaseModel

class ProfessorBase(BaseModel):
    name: str
    email: str | None = None
    ta_preferences: str | None = None

class ProfessorCreate(ProfessorBase):
    pass

class ProfessorRead(ProfessorBase):
    id: int

    class Config:
        orm_mode = True