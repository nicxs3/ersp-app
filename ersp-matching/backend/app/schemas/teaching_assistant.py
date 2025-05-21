from typing import Optional
from pydantic import BaseModel

class TeachingAssistantBase(BaseModel):
    name: str
    email: Optional[str] = None
    professor_preferences: Optional[str] = None

class TeachingAssistantCreate(TeachingAssistantBase):
    pass

class TeachingAssistantRead(TeachingAssistantBase):
    id: int

    class Config:
        orm_mode = True