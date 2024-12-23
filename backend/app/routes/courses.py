from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
import logging
from sqlalchemy.exc import SQLAlchemyError

from app.services.database import get_db
from app.services.auth import get_current_active_user
from app.models.user import User
from app.models.course import Course, Category
from app.schemas.course import CourseCreate, CourseUpdate

from pydantic import BaseModel

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

router = APIRouter()

class CourseResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    instructor: Optional[str]
    difficulty: Optional[str]
    categories: List[str] = []
    price: float
    averageRating: float
    totalEnrollments: int
    thumbnailUrl: Optional[str] = None

class PaginatedCourseResponse(BaseModel):
    courses: List[CourseResponse]
    total_count: int
    total_pages: int
    current_page: int

@router.post("", response_model=CourseResponse)
@router.post("/", response_model=CourseResponse)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    try:
        # Only instructors and admins can create courses
        if current_user.role not in ["instructor", "admin"]:
            raise HTTPException(status_code=403, detail="Not authorized to create courses")
        
        # Validate categories
        categories = []
        if course.category_ids:
            categories = db.query(Category).filter(Category.id.in_(course.category_ids)).all()
            if len(categories) != len(course.category_ids):
                raise HTTPException(status_code=400, detail="One or more categories not found")
        
        # Create course
        db_course = Course(
            title=course.title,
            description=course.description,
            instructor_id=current_user.id,
            difficulty_level=course.difficulty_level or 'Beginner'
        )
        
        # Add categories
        db_course.categories = categories
        
        db.add(db_course)
        db.commit()
        db.refresh(db_course)
        
        return db_course
    
    except SQLAlchemyError as e:
        logger.error(f"Database error in create_course: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in create_course: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("", response_model=PaginatedCourseResponse)
@router.get("/", response_model=PaginatedCourseResponse)
def list_courses(
    db: Session = Depends(get_db),
    category: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    pageSize: int = Query(9, ge=1, le=100),
    query: Optional[str] = Query(None)
):
    try:
        # Base query
        query_obj = db.query(Course).options(joinedload(Course.categories))
        
        # Apply filters
        if category:
            query_obj = query_obj.join(Course.categories).filter(Category.name == category)
        
        if difficulty:
            query_obj = query_obj.filter(Course.difficulty_level == difficulty)
        
        if query:
            query_obj = query_obj.filter(
                Course.title.ilike(f"%{query}%") | 
                Course.description.ilike(f"%{query}%")
            )
        
        # Only get active courses
        query_obj = query_obj.filter(Course.is_deleted == False)
        
        # Get total count for pagination
        total_count = query_obj.count()
        total_pages = (total_count + pageSize - 1) // pageSize
        
        # Calculate skip and limit
        skip = (page - 1) * pageSize
        
        # Get paginated results
        courses = query_obj.offset(skip).limit(pageSize).all()
        
        # Transform courses to match frontend expectations
        course_responses = [
            CourseResponse(
                id=str(course.id),
                title=course.title,
                description=course.description,
                instructor=course.instructor.username if course.instructor else None,
                difficulty=course.difficulty_level,
                categories=[cat.name for cat in course.categories],
                price=course.price,
                averageRating=course.average_rating or 0.0,
                totalEnrollments=course.total_enrollments or 0,
                thumbnailUrl=None  # Add logic for thumbnail if needed
            ) for course in courses
        ]
        
        return {
            "courses": course_responses,
            "total_count": total_count,
            "total_pages": total_pages,
            "current_page": page
        }
    
    except SQLAlchemyError as e:
        logger.error(f"Database error in list_courses: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in list_courses: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(
    course_id: int, 
    db: Session = Depends(get_db)
):
    try:
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        return course
    
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_course: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in get_course: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    course: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    try:
        # Find the course
        db_course = db.query(Course).filter(Course.id == course_id).first()
        
        # Check course exists
        if not db_course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        # Check permissions
        if db_course.instructor_id != current_user.id and current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Not authorized to update this course")
        
        # Validate and update categories if provided
        if course.category_ids is not None:
            categories = db.query(Category).filter(Category.id.in_(course.category_ids)).all()
            if len(categories) != len(course.category_ids):
                raise HTTPException(status_code=400, detail="One or more categories not found")
            db_course.categories = categories
        
        # Update other fields
        if course.title:
            db_course.title = course.title
        if course.description:
            db_course.description = course.description
        if course.difficulty_level:
            db_course.difficulty_level = course.difficulty_level
        
        db.commit()
        db.refresh(db_course)
        
        return db_course
    
    except SQLAlchemyError as e:
        logger.error(f"Database error in update_course: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in update_course: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/{course_id}", response_model=dict)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    try:
        # Find the course
        db_course = db.query(Course).filter(Course.id == course_id).first()
        
        # Check if course exists
        if not db_course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        # Check permissions (only course creator or admin can delete)
        if db_course.instructor_id != current_user.id and current_user.role != "admin":
            raise HTTPException(
                status_code=403, 
                detail="Not authorized to delete this course"
            )
        
        # Soft delete the course
        db_course.soft_delete()
        db.commit()
        
        return {"message": "Course successfully deleted"}
    
    except SQLAlchemyError as e:
        logger.error(f"Database error in delete_course: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in delete_course: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
