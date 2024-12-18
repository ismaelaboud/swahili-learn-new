import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models.user import User
from app.services.auth import get_password_hash

@pytest.fixture
def client():
    return TestClient(app)

def test_user_registration(client, test_db_session: Session):
    """Test user registration"""
    response = client.post("/users/register", json={
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "StrongPass123!",
        "full_name": "New User"
    })
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"

def test_user_login(client, test_db_session: Session, test_user):
    """Test user login"""
    response = client.post("/users/token", json={
        "username": test_user.username,
        "password": "password"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_get_user_profile(client, test_db_session: Session, test_user, test_access_token):
    """Test retrieving user profile"""
    headers = {"Authorization": f"Bearer {test_access_token}"}
    response = client.get("/users/me", headers=headers)
    
    print("Response data:", response.json())
    print("Test user:", test_user.username)
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == test_user.username

def test_update_user_profile(client, test_db_session: Session, test_user, test_access_token):
    """Test updating user profile"""
    headers = {"Authorization": f"Bearer {test_access_token}"}
    response = client.patch("/users/profile", 
        json={"full_name": "Updated Name"},
        headers=headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"

def test_password_reset_request(client, test_db_session: Session, test_user):
    """Test password reset request"""
    response = client.post("/users/password-reset-request", 
        json={"email": test_user.email}
    )
    
    assert response.status_code == 200
    assert "reset_token" in response.json()
