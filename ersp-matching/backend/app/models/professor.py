from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Professor(Base):
    __tablename__ = "professors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String)
    ta_preferences = Column(String)
#1