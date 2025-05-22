from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, List
import json

from app.db.session import get_db
from app.models.professor import Professor
from app.models.teaching_assistant import TeachingAssistant

router = APIRouter()

@router.get("/match")
@router.post("/match")
def match_students(db: Session = Depends(get_db)):
    # Get all professors and TAs from database
    professors = db.query(Professor).all()
    teaching_assistants = db.query(TeachingAssistant).all()

    # Convert string preferences to dictionaries
    course_prefs = {}
    student_prefs = {}
    
    for prof in professors:
        if prof.ta_preferences:
            try:
                # Try JSON first
                course_prefs[prof.name] = json.loads(prof.ta_preferences)
            except json.JSONDecodeError:
                # Fallback: comma-separated
                course_prefs[prof.name] = [x.strip() for x in prof.ta_preferences.split(',') if x.strip()]
    
    for ta in teaching_assistants:
        if ta.professor_preferences:
            try:
                student_prefs[ta.name] = json.loads(ta.professor_preferences)
            except json.JSONDecodeError:
                student_prefs[ta.name] = [x.strip() for x in ta.professor_preferences.split(',') if x.strip()]

    assignments = {}

    # Simple greedy algorithm:
    for ta, ta_courses in student_prefs.items():
        for course in ta_courses:
            if course in course_prefs and ta in course_prefs[course]:
                if course not in assignments.values():  # Course not taken
                    assignments[ta] = course
                    break

    return {"matches": assignments}