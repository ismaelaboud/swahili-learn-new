from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.services.database import get_db
from app.services.auth import get_current_active_user, get_current_admin_user
from app.models.user import User
from app.models.lesson import LessonModule
from app.schemas.lesson import (
    LessonModuleCreate, 
    LessonModuleResponse, 
    LessonModuleUpdate
)

router = APIRouter(
    prefix="/lessons",
    tags=["lessons"]
)

@router.post("/", response_model=LessonModuleResponse)
def create_lesson_module(
    lesson: LessonModuleCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Create a new lesson module
    - Only admins can create lesson modules
    - Requires valid course_id
    """
    # Validate course exists
    from app.models.course import Course
    course = db.query(Course).filter(Course.id == lesson.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Create lesson module
    db_lesson = LessonModule(
        course_id=lesson.course_id,
        title=lesson.title,
        description=lesson.description,
        content_type=lesson.content_type,
        content_url=lesson.content_url,
        order=lesson.order,
        is_interactive=lesson.is_interactive
    )
    
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    
    return db_lesson

@router.get("/course/{course_id}", response_model=List[LessonModuleResponse])
def get_course_lessons(
    course_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve all lesson modules for a specific course
    - Requires user to be logged in
    """
    # Validate course exists and user has access
    from app.models.course import Course
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Get lessons ordered by their sequence
    lessons = db.query(LessonModule).filter(
        LessonModule.course_id == course_id
    ).order_by(LessonModule.order).all()
    
    return lessons

@router.put("/{lesson_id}", response_model=LessonModuleResponse)
def update_lesson_module(
    lesson_id: int,
    lesson_update: LessonModuleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Update an existing lesson module
    - Only admins can update lesson modules
    """
    db_lesson = db.query(LessonModule).filter(LessonModule.id == lesson_id).first()
    if not db_lesson:
        raise HTTPException(status_code=404, detail="Lesson module not found")

    # Update lesson module fields
    for key, value in lesson_update.model_dump(exclude_unset=True).items():
        setattr(db_lesson, key, value)
    
    db.commit()
    db.refresh(db_lesson)
    
    return db_lesson

@router.delete("/{lesson_id}", status_code=204)
def delete_lesson_module(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Delete a lesson module
    - Only admins can delete lesson modules
    """
    db_lesson = db.query(LessonModule).filter(LessonModule.id == lesson_id).first()
    if not db_lesson:
        raise HTTPException(status_code=404, detail="Lesson module not found")

    db.delete(db_lesson)
    db.commit()
    
    return None
