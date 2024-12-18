from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime

from app.services.database import get_db
from app.services.auth import get_current_active_user
from app.models.user import User
from app.models.course import Course, Enrollment, Lesson, CourseProgress
from app.schemas.course import (
    LessonCreate, 
    LessonResponse, 
    CourseProgressCreate, 
    CourseProgressResponse
)

router = APIRouter()

@router.post("/lessons", response_model=LessonResponse)
def create_lesson(
    lesson: LessonCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Check if course exists and user is the instructor
    course = db.query(Course).filter(
        Course.id == lesson.course_id, 
        Course.instructor_id == current_user.id
    ).first()
    
    if not course:
        raise HTTPException(
            status_code=403, 
            detail="Not authorized to add lessons to this course"
        )
    
    # Create lesson
    db_lesson = Lesson(**lesson.dict())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    
    return db_lesson

@router.post("/track", response_model=CourseProgressResponse)
def update_lesson_progress(
    progress: CourseProgressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Verify enrollment
    enrollment = db.query(Enrollment).filter(
        Enrollment.id == progress.enrollment_id,
        Enrollment.user_id == current_user.id
    ).first()
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    # Check if lesson exists
    lesson = db.query(Lesson).filter(Lesson.id == progress.lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Find or create progress track
    db_progress = db.query(CourseProgress).filter(
        CourseProgress.enrollment_id == progress.enrollment_id,
        CourseProgress.lesson_id == progress.lesson_id
    ).first()
    
    if not db_progress:
        db_progress = CourseProgress(
            enrollment_id=progress.enrollment_id,
            lesson_id=progress.lesson_id
        )
        db.add(db_progress)
    
    # Update progress
    db_progress.completed = progress.completed
    db_progress.progress_percentage = progress.progress_percentage
    
    if progress.completed:
        db_progress.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_progress)
    
    return db_progress

@router.get("/course/{course_id}/progress", response_model=List[CourseProgressResponse])
def get_course_progress(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Find user's enrollment in the course
    enrollment = db.query(Enrollment).filter(
        Enrollment.course_id == course_id,
        Enrollment.user_id == current_user.id
    ).first()
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="Not enrolled in this course")
    
    # Get progress for all lessons in the course
    progress_tracks = db.query(CourseProgress).filter(
        CourseProgress.enrollment_id == enrollment.id
    ).options(
        joinedload(CourseProgress.lesson)
    ).all()
    
    return progress_tracks

@router.get("/overall/{enrollment_id}", response_model=dict)
def get_overall_course_progress(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Verify enrollment belongs to current user
    enrollment = db.query(Enrollment).filter(
        Enrollment.id == enrollment_id,
        Enrollment.user_id == current_user.id
    ).first()
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    # Count total and completed lessons
    total_lessons = db.query(Lesson).filter(
        Lesson.course_id == enrollment.course_id
    ).count()
    
    completed_lessons = db.query(CourseProgress).filter(
        CourseProgress.enrollment_id == enrollment_id,
        CourseProgress.completed == True
    ).count()
    
    # Calculate overall progress
    overall_progress = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
    
    return {
        "total_lessons": total_lessons,
        "completed_lessons": completed_lessons,
        "progress_percentage": round(overall_progress, 2)
    }
