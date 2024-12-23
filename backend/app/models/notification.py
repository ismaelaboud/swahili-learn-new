from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.services.database import Base

class Notification(Base):
    """
    Represents user notifications in the system
    """
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    message = Column(String, nullable=False)
    type = Column(String, nullable=False)  # e.g., 'course_enrollment', 'quiz_reminder'
    related_id = Column(Integer, nullable=True)  # ID of related entity (course, quiz, etc.)
    
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="notifications")
    
    def __repr__(self):
        return f"<Notification {self.id}: {self.message[:50]}>"
