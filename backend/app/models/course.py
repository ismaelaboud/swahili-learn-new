from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Table, Enum, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.services.database import Base
from app.models.assessment import Quiz
import enum

# Association table for many-to-many relationship
course_category_association = Table(
    'course_categories', Base.metadata,
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)

class EnrollmentStatus(enum.Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    DROPPED = "DROPPED"

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(EnrollmentStatus), default=EnrollmentStatus.PENDING)
    
    # Relationships
    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    progress_tracks = relationship("CourseProgress", back_populates="enrollment")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text, nullable=True)
    
    # Relationship with courses
    courses = relationship(
        "Course", 
        secondary=course_category_association, 
        back_populates="categories"
    )

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    instructor_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Difficulty Level
    difficulty_level = Column(String, default='Beginner')
    
    # Soft Delete Field
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)
    
    # Relationships
    categories = relationship(
        "Category", 
        secondary=course_category_association, 
        back_populates="courses"
    )
    enrollments = relationship("Enrollment", back_populates="course")
    lessons = relationship("Lesson", back_populates="course", order_by="Lesson.order")
    lesson_modules = relationship("LessonModule", back_populates="course", cascade="all, delete-orphan")
    quizzes = relationship("Quiz", back_populates="course")
    
    def soft_delete(self):
        """Mark course as deleted"""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()
    
    @classmethod
    def get_active_courses(cls, query):
        """Filter out deleted courses"""
        return query.filter(cls.is_deleted == False)

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    title = Column(String)
    description = Column(Text, nullable=True)
    order = Column(Integer)  # To maintain lesson sequence
    content_type = Column(String)  # e.g., 'video', 'text', 'quiz'
    content_url = Column(String, nullable=True)
    duration = Column(Integer, nullable=True)  # Duration in minutes
    
    # Relationships
    course = relationship("Course", back_populates="lessons")
    progress_tracks = relationship("CourseProgress", back_populates="lesson")

class CourseProgress(Base):
    __tablename__ = "course_progresses"

    id = Column(Integer, primary_key=True, index=True)
    enrollment_id = Column(Integer, ForeignKey('enrollments.id'))
    lesson_id = Column(Integer, ForeignKey('lessons.id'))
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    progress_percentage = Column(Float, default=0.0)
    
    # Relationships
    enrollment = relationship("Enrollment", back_populates="progress_tracks")
    lesson = relationship("Lesson", back_populates="progress_tracks")
