from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
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
    
    # Relationships
    course = relationship("Course", back_populates="lesson_modules")
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<LessonModule {self.title} (Type: {self.content_type})>"
