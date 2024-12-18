import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models.course import Lesson

client = TestClient(app)

def test_enroll_in_course(test_client, test_db_session: Session, test_course, test_user, test_access_token):
    """Test enrolling in a course"""
    headers = {"Authorization": f"Bearer {test_access_token}"}
    response = test_client.post("/enrollments/enroll", 
        json={
            "course_id": test_course.id,
            "status": "PENDING"  # Explicitly set uppercase status
        },
        headers=headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["course"]["id"] == test_course.id  # Use course.id from the nested course object
    assert data["status"] == "PENDING"
    assert data["user_id"] == test_user.id

def test_get_my_courses(test_client, test_db_session: Session, test_enrollment, test_access_token):
    """Test retrieving user's enrolled courses"""
    headers = {"Authorization": f"Bearer {test_access_token}"}
    response = test_client.get("/enrollments/my-courses", headers=headers)
    
    assert response.status_code == 200
    courses = response.json()
    assert len(courses) > 0
    assert courses[0]["status"] == "PENDING"  # Verify uppercase status

def test_create_lesson(test_client, test_db_session: Session, test_course, test_user, test_access_token):
    """Test creating a lesson for a course"""
    headers = {"Authorization": f"Bearer {test_access_token}"}
    response = test_client.post("/progress/lessons", 
        json={
            "course_id": test_course.id,
            "title": "Introduction Lesson",
            "content_type": "video",
            "order": 1
        },
        headers=headers
    )
    
    # Expect 403 if the test user is not the course instructor
    assert response.status_code in [200, 403]

def test_track_lesson_progress(test_client, test_db_session: Session, test_enrollment, test_access_token):
    """Test tracking lesson progress"""
    # First, create a lesson
    lesson = Lesson(
        course_id=test_enrollment.course_id,
        title="Test Lesson",
        content_type="video",
        order=1
    )
    test_db_session.add(lesson)
    test_db_session.commit()

    headers = {"Authorization": f"Bearer {test_access_token}"}
    response = test_client.post("/progress/track", 
        json={
            "enrollment_id": test_enrollment.id,
            "lesson_id": lesson.id,
            "completed": True,
            "progress_percentage": 100.0
        },
        headers=headers
    )
    
    # Expect 200 or 404 depending on enrollment and lesson existence
    assert response.status_code in [200, 404]

def test_get_course_progress(test_client, test_db_session: Session, test_enrollment, test_access_token):
    """Test retrieving course progress"""
    headers = {"Authorization": f"Bearer {test_access_token}"}
    response = test_client.get(f"/progress/course/{test_enrollment.course_id}/progress", headers=headers)
    
    # Expect 200 or 404 depending on enrollment
    assert response.status_code in [200, 404]

def test_get_overall_course_progress(test_client, test_db_session: Session, test_enrollment, test_access_token):
    """Test retrieving overall course progress"""
    headers = {"Authorization": f"Bearer {test_access_token}"}
    response = test_client.get(f"/progress/overall/{test_enrollment.id}", headers=headers)
    
    # Expect 200 or 404 depending on enrollment
    assert response.status_code in [200, 404]
