import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

def test_create_lesson_module(
    test_client: TestClient, 
    test_db_session: Session, 
    test_course, 
    test_admin_access_token
):
    """Test creating a lesson module"""
    lesson_data = {
        "course_id": test_course.id,
        "title": "Introduction to Swahili Greetings",
        "description": "Learn basic Swahili greetings",
        "content_type": "video",
        "content_url": "https://example.com/swahili-greetings.mp4",
        "order": 1,
        "is_interactive": False
    }
    
    response = test_client.post(
        "/lessons/", 
        json=lesson_data, 
        headers={"Authorization": f"Bearer {test_admin_access_token}"}
    )
    
    assert response.status_code == 200
    lesson = response.json()
    assert lesson["title"] == lesson_data["title"]
    assert lesson["content_type"] == lesson_data["content_type"]

def test_get_course_lessons(
    test_client: TestClient, 
    test_db_session: Session, 
    test_course, 
    test_access_token,
    test_admin_access_token
):
    """Test retrieving lessons for a course"""
    # First, create some lessons
    lesson_data1 = {
        "course_id": test_course.id,
        "title": "Lesson 1",
        "content_type": "text",
        "order": 1
    }
    lesson_data2 = {
        "course_id": test_course.id,
        "title": "Lesson 2",
        "content_type": "video",
        "order": 2
    }
    
    # Create lessons using admin token
    test_client.post(
        "/lessons/", 
        json=lesson_data1, 
        headers={"Authorization": f"Bearer {test_admin_access_token}"}
    )
    test_client.post(
        "/lessons/", 
        json=lesson_data2, 
        headers={"Authorization": f"Bearer {test_admin_access_token}"}
    )
    
    # Retrieve lessons
    response = test_client.get(
        f"/lessons/course/{test_course.id}", 
        headers={"Authorization": f"Bearer {test_access_token}"}
    )
    
    assert response.status_code == 200
    lessons = response.json()
    assert len(lessons) == 2
    assert lessons[0]["title"] == "Lesson 1"
    assert lessons[1]["title"] == "Lesson 2"

def test_update_lesson_module(
    test_client: TestClient, 
    test_db_session: Session, 
    test_course, 
    test_admin_access_token
):
    """Test updating a lesson module"""
    # First, create a lesson
    lesson_data = {
        "course_id": test_course.id,
        "title": "Original Lesson",
        "content_type": "text",
        "order": 1
    }
    
    create_response = test_client.post(
        "/lessons/", 
        json=lesson_data, 
        headers={"Authorization": f"Bearer {test_admin_access_token}"}
    )
    lesson = create_response.json()
    
    # Update the lesson
    update_data = {
        "title": "Updated Lesson",
        "description": "New description"
    }
    
    update_response = test_client.put(
        f"/lessons/{lesson['id']}", 
        json=update_data, 
        headers={"Authorization": f"Bearer {test_admin_access_token}"}
    )
    
    assert update_response.status_code == 200
    updated_lesson = update_response.json()
    assert updated_lesson["title"] == "Updated Lesson"
    assert updated_lesson["description"] == "New description"

def test_delete_lesson_module(
    test_client: TestClient, 
    test_db_session: Session, 
    test_course, 
    test_admin_access_token
):
    """Test deleting a lesson module"""
    # First, create a lesson
    lesson_data = {
        "course_id": test_course.id,
        "title": "Lesson to Delete",
        "content_type": "text",
        "order": 1
    }
    
    create_response = test_client.post(
        "/lessons/", 
        json=lesson_data, 
        headers={"Authorization": f"Bearer {test_admin_access_token}"}
    )
    lesson = create_response.json()
    
    # Delete the lesson
    delete_response = test_client.delete(
        f"/lessons/{lesson['id']}", 
        headers={"Authorization": f"Bearer {test_admin_access_token}"}
    )
    
    assert delete_response.status_code == 204
    
    # Verify lesson is deleted
    get_response = test_client.get(
        f"/lessons/course/{test_course.id}", 
        headers={"Authorization": f"Bearer {test_admin_access_token}"}
    )
    
    lessons = get_response.json()
    assert len(lessons) == 0
