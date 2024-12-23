from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.services.database import get_db
from app.services.lesson_service import LessonVisibilityService
from app.schemas.lesson import LessonVisibilityUpdate, LessonRead
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/lessons", tags=["lessons"])

@router.patch("/{lesson_id}/visibility", response_model=LessonRead)
def update_lesson_visibility(
    lesson_id: int,
    visibility_data: LessonVisibilityUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update lesson visibility settings
    
    Requires admin or instructor role
    """
    if current_user.role not in ['admin', 'instructor']:
        raise HTTPException(status_code=403, detail="Not authorized to update lesson visibility")
    
    try:
        updated_lesson = LessonVisibilityService.update_lesson_visibility(
            db, lesson_id, visibility_data
        )
        return updated_lesson
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/course/{course_id}/accessible", response_model=List[LessonRead])
def get_accessible_lessons(
    course_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get lessons accessible to the current user
    """
    accessible_lessons = LessonVisibilityService.get_accessible_lessons(
        db, course_id, current_user.role
    )
    return accessible_lessons
