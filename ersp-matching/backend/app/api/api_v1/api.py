from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, List
import json

from app.db.session import get_db
from app.models.professor import Professor
from app.models.teaching_assistant import TeachingAssistant
from app.classes import *
from app.valid_matching import *

router = APIRouter()

@router.get("/match")
@router.post("/match")
def match_students(db: Session = Depends(get_db)):
    # Get all professors and TAs from database
    professors = db.query(Professor).all()
    teaching_assistants = db.query(TeachingAssistant).all()

    ta_list = []
    for ta in teaching_assistants:
        ta_obj = Applicant(
            id=ta.name,  # or ta.id
            gpa=0,  # Fill with real data if available
            class_level=ta.class_level,  # Adjust as needed
            courses_taken=[],  # Fill with real data if available
            skills=[],         # Fill with real data if available
            prev_exp=[],       # Fill with real data if available
            pref_courses=[c.strip() for c in ta.professor_preferences.split(',')] if ta.professor_preferences else []
        )
        ta_list.append(ta_obj)

    course_list = []
    for prof in professors:
        course_obj = CourseRequirement(
            id=prof.name,
            attributes=[],  # Fill with real data if available
            required_ta_count=prof.req_tas,  # Make sure this column exists
            pref_tas=[c.strip() for c in prof.ta_preferences.split(',')] if prof.ta_preferences else []
        )
        course_list.append(course_obj)

    # Use your valid_matching.py functions
    courses, edges, ta_list = get_courses_and_edges(course_list, ta_list)
    final_graph = complete_matching(ta_list, courses, edges)

    # Format the result
    if final_graph is None:
        return {"matches": None, "message": "No valid matching found"}
    else:
        matches = []
        for ta in final_graph.tas:
            matched_course = final_graph.curr_match.get(ta)
            if matched_course:
                matches.append({"ta": ta.id, "course": matched_course.id})
        return {"matches": matches}



    '''
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
    '''