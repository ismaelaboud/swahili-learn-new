from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta, timezone
from app.services.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    role = Column(String, default="student")
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    
    # Password Reset Fields
    reset_token = Column(String, nullable=True)
    reset_token_expiration = Column(DateTime, nullable=True)
    
    # Relationships
    enrollments = relationship("Enrollment", back_populates="user")
    
    def generate_reset_token(self):
        """Generate a reset token valid for 1 hour"""
        import secrets
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expiration = datetime.now(timezone.utc) + timedelta(hours=1)
        return self.reset_token
    
    def is_reset_token_valid(self):
        """Check if reset token is valid and not expired"""
        return (self.reset_token is not None and 
                self.reset_token_expiration is not None and 
                datetime.now(timezone.utc) < self.reset_token_expiration)
