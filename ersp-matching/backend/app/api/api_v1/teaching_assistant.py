from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.teaching_assistant import TeachingAssistant
from app.schemas.teaching_assistant import TeachingAssistantCreate, TeachingAssistantRead
from typing import List

router = APIRouter()

@router.post("/", response_model=TeachingAssistantRead)
def create_teaching_assistant(ta: TeachingAssistantCreate, db: Session = Depends(get_db)):
    db_ta = TeachingAssistant(**ta.dict())
    db.add(db_ta)
    db.commit()
    db.refresh(db_ta)
    return db_ta

@router.get("/", response_model=List[TeachingAssistantRead])
def read_teaching_assistants(db: Session = Depends(get_db)):
    return db.query(TeachingAssistant).all()

@router.get("/{ta_id}", response_model=TeachingAssistantRead)
def read_teaching_assistant(ta_id: int, db: Session = Depends(get_db)):
    ta = db.query(TeachingAssistant).filter(TeachingAssistant.id == ta_id).first()
    if not ta:
        raise HTTPException(status_code=404, detail="Teaching Assistant not found")
    return ta