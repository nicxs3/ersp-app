from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.professor import Professor
from app.schemas.professor import ProfessorCreate, ProfessorRead
from typing import List

router = APIRouter()

@router.post("/", response_model=ProfessorRead)
def create_professor(prof: ProfessorCreate, db: Session = Depends(get_db)):
    db_prof = Professor(**prof.dict())
    db.add(db_prof)
    db.commit()
    db.refresh(db_prof)
    return db_prof

@router.get("/", response_model=List[ProfessorRead])
def read_professors(db: Session = Depends(get_db)):
    return db.query(Professor).all()

@router.get("/{professor_id}", response_model=ProfessorRead)
def read_professor(professor_id: int, db: Session = Depends(get_db)):
    prof = db.query(Professor).filter(Professor.id == professor_id).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Professor not found")
    return prof