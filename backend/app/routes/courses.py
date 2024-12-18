from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from app.services.database import get_db
from app.services.auth import get_current_active_user
from app.models.user import User
from app.models.course import Course, Category
from app.schemas.course import CourseCreate, CourseResponse, CourseUpdate

router = APIRouter()

@router.post("/", response_model=CourseResponse)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
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

@router.get("/", response_model=List[CourseResponse])
def list_courses(
    db: Session = Depends(get_db),
    category: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    skip: int = 0, 
    limit: int = 100
):
    # Base query
    query = db.query(Course).options(joinedload(Course.categories))
    
    # Apply filters
    if category:
        query = query.join(Course.categories).filter(Category.name == category)
    
    if difficulty:
        query = query.filter(Course.difficulty_level == difficulty)
    
    # Only get active courses
    query = Course.get_active_courses(query)
    
    return query.offset(skip).limit(limit).all()

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(
    course_id: int, 
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    course: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
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

@router.delete("/{course_id}", response_model=dict)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
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
