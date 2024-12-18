from pydantic import BaseModel, Field, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)

class LessonModuleUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200, description="Title of the lesson module")
    description: Optional[str] = Field(None, description="Description of the lesson module")
    content_type: Optional[LessonContentType] = Field(None, description="Type of content for the lesson")
    content_url: Optional[str] = Field(None, description="URL or path to the lesson content")
    order: Optional[int] = Field(None, ge=0, description="Order of the lesson in the course")
    is_interactive: Optional[bool] = Field(None, description="Whether the lesson is interactive")
