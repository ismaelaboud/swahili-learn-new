from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.services.database import Base

class Certificate(Base):
    """
    Represents course completion certificates
    """
    __tablename__ = "certificates"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    
    certificate_id = Column(String, unique=True, nullable=False, index=True)
    issued_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
    course = relationship("Course")
    
    def __repr__(self):
        return f"<Certificate {self.certificate_id} for {self.user.username} - {self.course.title}>"
