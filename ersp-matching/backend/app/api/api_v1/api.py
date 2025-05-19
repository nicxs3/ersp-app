from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, List

router = APIRouter()

# Define request format
class Preferences(BaseModel):
    course_preferences: Dict[str, List[str]]
    student_preferences: Dict[str, List[str]]

@router.post("/match")
def match_students(preferences: Preferences):
    course_prefs = preferences.course_preferences
    student_prefs = preferences.student_preferences

    assignments = {}

    # Simple greedy algorithm:
    for ta, ta_courses in student_prefs.items():
        for course in ta_courses:
            if course in course_prefs and ta in course_prefs[course]:
                if course not in assignments.values():  # Course not taken
                    assignments[ta] = course
                    break

    return {"matches": assignments}