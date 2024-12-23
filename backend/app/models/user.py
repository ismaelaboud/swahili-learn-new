from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta, timezone
import enum

from app.services.database import Base

class UserRoleEnum(enum.Enum):
    GUEST = "guest"
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    role = Column(Enum(UserRoleEnum), default=UserRoleEnum.STUDENT)
    
    # Time-based access tracking
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    last_login = Column(DateTime, nullable=True)
    
    # Password Reset Fields
    reset_token = Column(String, nullable=True)
    reset_token_expiration = Column(DateTime, nullable=True)
    
    # Relationships
    enrollments = relationship("Enrollment", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    lesson_progresses = relationship("LessonProgress", back_populates="user")
    
    # Courses taught (for instructors)
    courses_taught = relationship("Course", back_populates="instructor")
    
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

    def is_active(self):
        """
        Check if user account is active based on various conditions
        """
        # Add more complex logic as needed
        return True
    
    def has_access_to_course(self, course):
        """
        Determine if user has access to a specific course
        """
        from app.security.access_control import AccessControl, UserRole, PermissionLevel
        
        # Convert enum to match AccessControl
        role_map = {
            UserRoleEnum.GUEST: UserRole.GUEST,
            UserRoleEnum.STUDENT: UserRole.STUDENT,
            UserRoleEnum.INSTRUCTOR: UserRole.INSTRUCTOR,
            UserRoleEnum.ADMIN: UserRole.ADMIN
        }
        
        return AccessControl.check_permission(
            role_map[self.role], 
            'courses', 
            PermissionLevel.READ
        )
