import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models.course import Course

client = TestClient(app)

def test_create_course(test_client, test_db_session: Session, test_category, test_access_token):
    """Test course creation"""
    response = test_client.post("/courses/", 
        json={
            "title": "Python Fundamentals",
            "description": "Learn Python from scratch",
            "difficulty_level": "Beginner",
            "category_ids": [test_category.id]
        },
        headers={"Authorization": f"Bearer {test_access_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Python Fundamentals"
    assert len(data["categories"]) == 1
    assert data["categories"][0]["name"] == test_category.name

def test_list_courses(test_client, test_db_session: Session, test_course):
    """Test listing courses"""
    response = test_client.get("/courses/")
    
    assert response.status_code == 200
    courses = response.json()
    assert len(courses) > 0

def test_get_single_course(test_client, test_db_session: Session, test_course):
    """Test retrieving a single course"""
    response = test_client.get(f"/courses/{test_course.id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_course.id
    assert data["title"] == test_course.title

def test_update_course(test_client, test_db_session: Session, test_course, test_category, test_access_token):
    """Test updating a course"""
    response = test_client.put(f"/courses/{test_course.id}", 
        json={
            "title": "Updated Course Title",
            "description": "Updated description",
            "category_ids": [test_category.id]
        },
        headers={"Authorization": f"Bearer {test_access_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Course Title"
    assert len(data["categories"]) == 1

def test_delete_course(test_client, test_db_session: Session, test_course, test_access_token):
    """Test soft deleting a course"""
    response = test_client.delete(f"/courses/{test_course.id}", 
        headers={"Authorization": f"Bearer {test_access_token}"}
    )
    
    assert response.status_code == 200
    assert "message" in response.json()
