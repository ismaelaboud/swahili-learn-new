import os
import sys
import uuid
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from app.models.lesson import LessonModule

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from fastapi import Depends
from fastapi import HTTPException

from app.main import app
from app.services.database import Base, get_db
from app.services.auth import get_current_active_user, get_password_hash
from app.models.user import User
from app.models.course import Course, Category, Enrollment, EnrollmentStatus, Lesson
from app.models.lesson import LessonModule
from app.models.user import UserRoleEnum  # Import UserRoleEnum

# Create an in-memory SQLite engine for testing
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override database dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Create test database and tables
@pytest.fixture(scope="session")
def test_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all tables
    Base.metadata.drop_all(bind=engine)

# Override authentication dependency
def override_get_current_active_user(db: Session = Depends(get_db)):
    # Use the test user from the current session
    # This is a hack to work around the test environment
    # We'll retrieve the last created test user
    test_user = db.query(User).filter(User.username.like('testuser_%')).order_by(User.id.desc()).first()
    if not test_user:
        raise HTTPException(status_code=404, detail="Test user not found")
    return test_user

# Generate test access token
def create_test_access_token(username: str, expires_delta: Optional[timedelta] = None):
    to_encode = {"sub": username}
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, "test_secret_key", algorithm="HS256")

# Override app dependencies for testing
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_active_user] = override_get_current_active_user

# Test client fixture
@pytest.fixture
def test_client():
    return TestClient(app)

# Database session fixture
@pytest.fixture
def test_db_session(test_db):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    # Ensure tables are created
    Base.metadata.create_all(bind=engine)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

# Test user fixture
@pytest.fixture
def test_user(test_db_session):
    unique_email = f"test{uuid.uuid4()}@example.com"
    user = User(
        username=f"testuser_{uuid.uuid4()}",
        email=unique_email,
        role=UserRoleEnum.ADMIN,  # Use the enum value
        hashed_password=get_password_hash("password")  
    )
    test_db_session.add(user)
    test_db_session.commit()
    test_db_session.refresh(user)
    return user

# Test access token fixture
@pytest.fixture
def test_access_token(test_user):
    return create_test_access_token(test_user.username)

# Test admin access token fixture
@pytest.fixture
def test_admin_access_token(test_user):
    """
    Create an access token for an admin user
    """
    return create_test_access_token(test_user.username)

# Test category fixture
@pytest.fixture
def test_category(test_db_session):
    category = Category(name=f"Test Category {uuid.uuid4()}", description="Test Category Description")
    test_db_session.add(category)
    test_db_session.commit()
    test_db_session.refresh(category)
    return category

# Test course fixture
@pytest.fixture
def test_course(test_db_session, test_category, test_user):
    course = Course(
        title="Python Programming", 
        description="Learn Python from scratch",
        instructor_id=test_user.id,  # Ensure the course is created by the test user
        difficulty_level="beginner",
        tags="python,programming,beginner",
        category="Web Development",
        price=49.99,
        average_rating=4.5,
        total_enrollments=100
    )
    course.categories.append(test_category)
    test_db_session.add(course)
    test_db_session.commit()
    test_db_session.refresh(course)
    return course

# Fixture to create multiple test courses for pagination
@pytest.fixture
def test_courses(test_db_session, test_category, test_user):
    courses = [
        Course(
            title=f"Python Course {i}", 
            description=f"Python programming course {i}",
            instructor_id=test_user.id,
            difficulty_level="beginner" if i % 2 == 0 else "intermediate",
            tags=f"python,programming,course{i}",
            category="Web Development" if i % 2 == 0 else "Data Science",
            price=float(i * 10),
            average_rating=float(i % 5),
            total_enrollments=i * 10
        ) for i in range(1, 11)  # Create 10 courses
    ]
    
    for course in courses:
        course.categories.append(test_category)
        test_db_session.add(course)
    
    test_db_session.commit()
    
    # Refresh each course to ensure it has an ID
    for course in courses:
        test_db_session.refresh(course)
    
    return courses

# Test enrollment fixture
@pytest.fixture
def test_enrollment(test_db_session, test_course, test_user):
    enrollment = Enrollment(
        user_id=test_user.id,
        course_id=test_course.id,
        status=EnrollmentStatus.PENDING  # Use uppercase PENDING
    )
    test_db_session.add(enrollment)
    test_db_session.commit()
    test_db_session.refresh(enrollment)
    return enrollment
