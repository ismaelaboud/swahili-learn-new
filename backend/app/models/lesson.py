from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, JSON, ARRAY, Enum
from sqlalchemy.orm import relationship
from app.services.database import Base
from datetime import datetime

class LessonModule(Base):
    __tablename__ = 'lesson_modules'
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    content_type = Column(String(50), nullable=False)  # 'video', 'audio', 'pdf', 'text'
    content_url = Column(String(500), nullable=True)
    order = Column(Integer, default=0)
    is_interactive = Column(Boolean, default=False)
    
    # New Visibility Controls
    is_visible = Column(Boolean, default=True)
    visibility_start_date = Column(DateTime, nullable=True)
    visibility_end_date = Column(DateTime, nullable=True)
    required_roles = Column(JSON, default=['student'])
    
    # Add skill tags and difficulty level
    skill_tags = Column(JSON, nullable=True)  # Store list of skill tags
    difficulty_level = Column(Enum('beginner', 'intermediate', 'advanced'), default='beginner')
    
    # Relationships
    course = relationship("Course", back_populates="lesson_modules")
    lesson_progresses = relationship("LessonProgress", back_populates="lesson")
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def is_accessible(self, user_role):
        """
        Check if the lesson is accessible based on visibility rules
        """
        now = datetime.utcnow()
        
        # Check if lesson is generally visible
        if not self.is_visible:
            return False
        
        # Check start date visibility
        if self.visibility_start_date and now < self.visibility_start_date:
            return False
        
        # Check end date visibility
        if self.visibility_end_date and now > self.visibility_end_date:
            return False
        
        # Check user role access
        if user_role not in self.required_roles:
            return False
        
        return True

    def __repr__(self):
        return f"<LessonModule {self.title} (Type: {self.content_type})>"
