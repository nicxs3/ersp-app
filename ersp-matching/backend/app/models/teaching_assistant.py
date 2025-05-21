from sqlalchemy import Column, Integer, String
from app.db.session import Base

class TeachingAssistant(Base):
    __tablename__ = "teaching_assistants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String)
    professor_preferences = Column(String)