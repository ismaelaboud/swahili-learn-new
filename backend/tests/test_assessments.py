import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

def test_create_quiz(
    test_client: TestClient, 
    test_db_session: Session, 
    test_course, 
    test_admin_access_token
):
    """Test creating a quiz"""
    quiz_data = {
        "course_id": test_course.id,
        "title": "Swahili Basics Quiz",
        "description": "Test your basic Swahili knowledge",
        "duration_minutes": 30,
        "passing_score": 0.7,
        "is_timed": True,
        "questions": [
            {
                "question_text": "What does 'Jambo' mean?",
                "question_type": "multiple_choice",
                "points": 1.0,
                "choices": [
                    {"choice_text": "Hello", "is_correct": True},
                    {"choice_text": "Goodbye", "is_correct": False},
                    {"choice_text": "Thank you", "is_correct": False}
                ]
            },
            {
                "question_text": "Is Swahili an official language in Tanzania?",
                "question_type": "true_false",
                "points": 1.0,
                "choices": [
                    {"choice_text": "True", "is_correct": True},
                    {"choice_text": "False", "is_correct": False}
                ]
            }
        ]
    }
    
    response = test_client.post(
        "/quizzes/", 
        json=quiz_data, 
        headers={"Authorization": f"Bearer {test_admin_access_token}"}
    )
    
    assert response.status_code == 200
    quiz = response.json()
    assert quiz["title"] == quiz_data["title"]
    assert len(quiz["questions"]) == 2

def test_get_course_quizzes(
    test_client: TestClient, 
    test_db_session: Session, 
    test_course, 
    test_admin_access_token,
    test_access_token
):
    """Test retrieving quizzes for a course"""
    # First, create a quiz
    quiz_data = {
        "course_id": test_course.id,
        "title": "Swahili Intermediate Quiz",
        "questions": [
            {
                "question_text": "What is 'maji' in English?",
                "question_type": "multiple_choice",
                "points": 1.0,
                "choices": [
                    {"choice_text": "Water", "is_correct": True},
                    {"choice_text": "Food", "is_correct": False}
                ]
            }
        ]
    }
    
    test_client.post(
        "/quizzes/", 
        json=quiz_data, 
        headers={"Authorization": f"Bearer {test_admin_access_token}"}
    )
    
    # Retrieve quizzes
    response = test_client.get(
        f"/quizzes/course/{test_course.id}", 
        headers={"Authorization": f"Bearer {test_access_token}"}
    )
    
    assert response.status_code == 200
    quizzes = response.json()
    assert len(quizzes) > 0
    assert quizzes[0]["title"] == "Swahili Intermediate Quiz"

def test_submit_quiz(
    test_client: TestClient, 
    test_db_session: Session, 
    test_course, 
    test_admin_access_token,
    test_access_token,
    test_user
):
    """Test submitting a quiz"""
    # First, create a quiz
    quiz_data = {
        "course_id": test_course.id,
        "title": "Swahili Final Quiz",
        "questions": [
            {
                "question_text": "What is 'Habari'?",
                "question_type": "multiple_choice",
                "points": 1.0,
                "choices": [
                    {"choice_text": "Hello", "is_correct": True},
                    {"choice_text": "Goodbye", "is_correct": False},
                    {"choice_text": "Thank you", "is_correct": False}
                ]
            }
        ]
    }
    
    create_response = test_client.post(
        "/quizzes/", 
        json=quiz_data, 
        headers={"Authorization": f"Bearer {test_admin_access_token}"}
    )
    quiz = create_response.json()
    
    # Submit quiz
    submission_data = {
        "quiz_id": quiz["id"],
        "answers": [
            {
                "question_id": quiz["questions"][0]["id"],
                "user_answer": "Hello"
            }
        ]
    }
    
    response = test_client.post(
        "/quizzes/submit", 
        json=submission_data, 
        headers={"Authorization": f"Bearer {test_access_token}"}
    )
    
    assert response.status_code == 200
    submission = response.json()
    assert submission["quiz_id"] == quiz["id"]
    assert submission["user_id"] == test_user.id
    assert submission["is_passed"] is True

def test_get_quiz_submission_result(
    test_client: TestClient, 
    test_db_session: Session, 
    test_course, 
    test_admin_access_token,
    test_access_token
):
    """Test retrieving quiz submission results"""
    # First, create and submit a quiz
    quiz_data = {
        "course_id": test_course.id,
        "title": "Swahili Result Quiz",
        "questions": [
            {
                "question_text": "What is 'Asante'?",
                "question_type": "multiple_choice",
                "points": 1.0,
                "choices": [
                    {"choice_text": "Thank you", "is_correct": True},
                    {"choice_text": "Hello", "is_correct": False}
                ]
            }
        ]
    }
    
    create_response = test_client.post(
        "/quizzes/", 
        json=quiz_data, 
        headers={"Authorization": f"Bearer {test_admin_access_token}"}
    )
    quiz = create_response.json()
    
    # Submit quiz
    submission_data = {
        "quiz_id": quiz["id"],
        "answers": [
            {
                "question_id": quiz["questions"][0]["id"],
                "user_answer": "Thank you"
            }
        ]
    }
    
    test_client.post(
        "/quizzes/submit", 
        json=submission_data, 
        headers={"Authorization": f"Bearer {test_access_token}"}
    )
    
    # Get submission result
    response = test_client.get(
        f"/quizzes/{quiz['id']}/results", 
        headers={"Authorization": f"Bearer {test_access_token}"}
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["quiz_id"] == quiz["id"]
    assert result["is_passed"] is True
