from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.services.database import get_db
from app.services.auth import get_current_active_user
from app.models.user import User
from app.models.course import Course, Enrollment, EnrollmentStatus
from app.schemas.course import EnrollmentCreate, EnrollmentResponse

router = APIRouter()

@router.post("/enroll", response_model=EnrollmentResponse)
def enroll_in_course(
    enrollment: EnrollmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Check if course exists
    course = db.query(Course).filter(Course.id == enrollment.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check if user is already enrolled
    existing_enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id, 
        Enrollment.course_id == enrollment.course_id
    ).first()
    
    if existing_enrollment:
        raise HTTPException(
            status_code=400, 
            detail="Already enrolled in this course"
        )
    
    # Create new enrollment
    db_enrollment = Enrollment(
        user_id=current_user.id,
        course_id=enrollment.course_id,
        status=enrollment.status or EnrollmentStatus.PENDING
    )
    
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    
    return db_enrollment

@router.get("/my-courses", response_model=List[EnrollmentResponse])
def get_my_courses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Get all enrollments for the current user, including course details
    enrollments = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id
    ).options(
        joinedload(Enrollment.course)
    ).all()
    
    return enrollments

@router.patch("/update-status/{enrollment_id}", response_model=EnrollmentResponse)
def update_enrollment_status(
    enrollment_id: int,
    status: EnrollmentStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Find the enrollment
    db_enrollment = db.query(Enrollment).filter(
        Enrollment.id == enrollment_id,
        Enrollment.user_id == current_user.id
    ).first()
    
    if not db_enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    # Update status
    db_enrollment.status = status
    db.commit()
    db.refresh(db_enrollment)
    
    return db_enrollment
