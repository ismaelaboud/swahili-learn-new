from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.services.database import Base

class LessonProgress(Base):
    """
    Tracks individual user's progress through lessons
    """
    __tablename__ = "lesson_progresses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    lesson_id = Column(Integer, ForeignKey('lesson_modules.id'), nullable=False)
    
    # Progress tracking
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    is_completed = Column(Boolean, default=False)
    
    # Time spent on lesson
    total_time_spent = Column(Integer, default=0)  # in seconds
    
    # Relationships
    user = relationship("User", back_populates="lesson_progresses")
    lesson = relationship("LessonModule", back_populates="lesson_progresses")
    
    def mark_completed(self):
        """
        Mark lesson as completed
        """
        self.is_completed = True
        self.completed_at = datetime.utcnow()
    
    def update_time_spent(self, time_spent: int):
        """
        Update total time spent on lesson
        
        :param time_spent: Time spent in seconds
        """
        self.total_time_spent += time_spent
