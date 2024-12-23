from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class LessonContentType(str, Enum):
    VIDEO = "video"
    AUDIO = "audio"
    PDF = "pdf"
    TEXT = "text"

class LessonModuleBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200, description="Title of the lesson module")
    description: Optional[str] = Field(None, description="Description of the lesson module")
    content_type: LessonContentType = Field(..., description="Type of content for the lesson")
    content_url: Optional[str] = Field(None, description="URL or path to the lesson content")
    order: int = Field(default=0, ge=0, description="Order of the lesson in the course")
    is_interactive: bool = Field(default=False, description="Whether the lesson is interactive")

class LessonModuleCreate(LessonModuleBase):
    course_id: int = Field(..., description="ID of the course this lesson belongs to")

class LessonModuleResponse(LessonModuleBase):
    id: int
    course_id: int
    created_at: datetime
    updated_at: datetime
    
    # New visibility fields
    is_visible: bool = Field(default=True, description="Whether the lesson is currently visible")
    visibility_start_date: Optional[datetime] = Field(None, description="Start date of lesson visibility")
    visibility_end_date: Optional[datetime] = Field(None, description="End date of lesson visibility")
    required_roles: List[str] = Field(default=['student'], description="Roles allowed to access this lesson")

    model_config = ConfigDict(from_attributes=True)

class LessonModuleUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200, description="Title of the lesson module")
    description: Optional[str] = Field(None, description="Description of the lesson module")
    content_type: Optional[LessonContentType] = Field(None, description="Type of content for the lesson")
    content_url: Optional[str] = Field(None, description="URL or path to the lesson content")
    order: Optional[int] = Field(None, ge=0, description="Order of the lesson in the course")
    is_interactive: Optional[bool] = Field(None, description="Whether the lesson is interactive")

class LessonVisibilityUpdate(BaseModel):
    is_visible: Optional[bool] = True
    visibility_start_date: Optional[datetime] = None
    visibility_end_date: Optional[datetime] = None
    required_roles: Optional[List[str]] = ['student']

    def __init__(self, **data):
        """
        Custom initialization to validate dates
        """
        # Validate date range
        if (data.get('visibility_start_date') and 
            data.get('visibility_end_date') and 
            data.get('visibility_start_date') >= data.get('visibility_end_date')):
            raise ValueError("End date must be after start date")
        
        # Validate roles
        if data.get('required_roles') is not None and len(data.get('required_roles')) == 0:
            raise ValueError("At least one role must be specified")
        
        super().__init__(**data)

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        extra='forbid',
        validate_default=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            'example': {
                'is_visible': True,
                'visibility_start_date': '2024-01-01T00:00:00',
                'visibility_end_date': '2024-12-31T23:59:59',
                'required_roles': ['student', 'admin']
            }
        }
    )
