from pydantic import BaseModel, Field, validator, field_validator, ConfigDict
from typing import List, Optional
from datetime import datetime
from enum import Enum

# Category Schemas
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        orm_mode = True

# Updated Course Schemas
class CourseBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    difficulty_level: Optional[str] = Field(
        default='Beginner', 
        pattern='^(Beginner|Intermediate|Advanced)$'
    )
    category_ids: Optional[List[int]] = []

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int
    instructor_id: int
    created_at: datetime
    updated_at: datetime
    categories: List[CategoryResponse] = []

    model_config = ConfigDict(orm_mode=True)

# Additional validation
@field_validator('difficulty_level')
@classmethod
def validate_difficulty_level(cls, v):
    valid_levels = ['Beginner', 'Intermediate', 'Advanced']
    if v not in valid_levels:
        raise ValueError(f'Difficulty level must be one of {valid_levels}')
    return v

class EnrollmentStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    DROPPED = "DROPPED"

class EnrollmentBase(BaseModel):
    course_id: int
    status: Optional[EnrollmentStatus] = EnrollmentStatus.PENDING

class EnrollmentCreate(EnrollmentBase):
    pass

class LessonBase(BaseModel):
    title: str
    description: Optional[str] = None
    order: int
    content_type: str = Field(..., description="Type of lesson content")
    content_url: Optional[str] = None
    duration: Optional[int] = None  # Duration in minutes

class LessonCreate(LessonBase):
    course_id: int

class LessonResponse(LessonBase):
    id: int
    course_id: int

    class Config:
        from_attributes = True

class CourseProgressBase(BaseModel):
    lesson_id: int
    completed: Optional[bool] = False
    progress_percentage: Optional[float] = 0.0

class CourseProgressCreate(CourseProgressBase):
    enrollment_id: int

class CourseProgressResponse(CourseProgressBase):
    id: int
    completed_at: Optional[datetime] = None
    lesson: Optional[LessonResponse] = None

    class Config:
        from_attributes = True

class EnrollmentResponse(BaseModel):
    id: int
    user_id: int
    enrolled_at: datetime
    status: EnrollmentStatus
    progress_tracks: List[CourseProgressResponse] = []
    course: Optional[CourseResponse] = None

    class Config:
        from_attributes = True
