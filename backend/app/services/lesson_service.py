from sqlalchemy.orm import Session
from datetime import datetime
from app.models.lesson import LessonModule
from app.schemas.lesson import LessonVisibilityUpdate
from typing import List

class LessonVisibilityService:
    @staticmethod
    def validate_visibility_update(visibility_data: LessonVisibilityUpdate):
        """
        Validate visibility update parameters
        
        Args:
            visibility_data (LessonVisibilityUpdate): Visibility update data
        
        Raises:
            ValueError: If validation fails
        """
        # Validate date range
        if (visibility_data.visibility_start_date and 
            visibility_data.visibility_end_date and 
            visibility_data.visibility_start_date >= visibility_data.visibility_end_date):
            raise ValueError("End date must be after start date")
        
        # Validate roles
        if not visibility_data.required_roles:
            raise ValueError("At least one role must be specified")

    @staticmethod
    def update_lesson_visibility(
        db: Session, 
        lesson_id: int, 
        visibility_data: LessonVisibilityUpdate
    ):
        """
        Update lesson visibility settings
        
        Args:
            db (Session): Database session
            lesson_id (int): ID of the lesson to update
            visibility_data (LessonVisibilityUpdate): Visibility update data
        
        Returns:
            LessonModule: Updated lesson module
        """
        # Validate input
        LessonVisibilityService.validate_visibility_update(visibility_data)
        
        lesson = db.query(LessonModule).filter(LessonModule.id == lesson_id).first()
        
        if not lesson:
            raise ValueError(f"Lesson with ID {lesson_id} not found")
        
        # Update visibility fields
        if visibility_data.is_visible is not None:
            lesson.is_visible = visibility_data.is_visible
        
        if visibility_data.visibility_start_date is not None:
            lesson.visibility_start_date = visibility_data.visibility_start_date
        
        if visibility_data.visibility_end_date is not None:
            lesson.visibility_end_date = visibility_data.visibility_end_date
        
        if visibility_data.required_roles is not None:
            lesson.required_roles = visibility_data.required_roles
        
        db.commit()
        db.refresh(lesson)
        
        return lesson
    
    @staticmethod
    def get_accessible_lessons(
        db: Session, 
        course_id: int, 
        user_role: str
    ):
        """
        Get lessons accessible to a specific user role
        
        Args:
            db (Session): Database session
            course_id (int): Course ID to filter lessons
            user_role (str): User role to check accessibility
        
        Returns:
            List[LessonModule]: List of accessible lessons
        """
        now = datetime.utcnow()
        
        accessible_lessons = db.query(LessonModule).filter(
            LessonModule.course_id == course_id,
            LessonModule.is_visible == True,
            # Start date check
            (LessonModule.visibility_start_date.is_(None) | 
             (LessonModule.visibility_start_date <= now)),
            # End date check
            (LessonModule.visibility_end_date.is_(None) | 
             (LessonModule.visibility_end_date >= now)),
            # Role check
            LessonModule.required_roles.contains([user_role])
        ).all()
        
        return accessible_lessons
