import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.lesson import LessonModule
from app.models.course import Course
from app.services.lesson_service import LessonVisibilityService
from app.schemas.lesson import LessonVisibilityUpdate

def test_lesson_visibility_update(test_db_session: Session, test_course: Course):
    """
    Test updating lesson visibility settings
    """
    # Create a sample lesson for the test course
    sample_lesson = LessonModule(
        course_id=test_course.id,
        title="Test Lesson",
        is_visible=True,
        content_type="text",
        required_roles=["student"]
    )
    test_db_session.add(sample_lesson)
    test_db_session.commit()
    
    visibility_update = LessonVisibilityUpdate(
        is_visible=False,
        visibility_start_date=datetime.utcnow() + timedelta(days=1),
        visibility_end_date=datetime.utcnow() + timedelta(days=30),
        required_roles=['instructor']
    )
    
    updated_lesson = LessonVisibilityService.update_lesson_visibility(
        test_db_session, sample_lesson.id, visibility_update
    )
    
    assert updated_lesson.is_visible == False
    assert updated_lesson.required_roles == ['instructor']
    assert updated_lesson.visibility_start_date is not None
    assert updated_lesson.visibility_end_date is not None

def test_lesson_visibility_validation(test_db_session: Session, test_course: Course):
    """
    Test validation of lesson visibility settings
    """
    # Create a sample lesson for the test course
    sample_lesson = LessonModule(
        course_id=test_course.id,
        title="Test Lesson",
        is_visible=True,
        content_type="text",
        required_roles=["student"]
    )
    test_db_session.add(sample_lesson)
    test_db_session.commit()
    
    # Test invalid date range
    start_date = datetime.utcnow() + timedelta(days=30)
    end_date = datetime.utcnow() + timedelta(days=1)
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")
    
    with pytest.raises(ValueError, match="End date must be after start date"):
        LessonVisibilityUpdate(
            visibility_start_date=start_date,
            visibility_end_date=end_date
        )
    
    # Test empty roles
    with pytest.raises(ValueError, match="At least one role must be specified"):
        LessonVisibilityUpdate(required_roles=[])

def test_lesson_accessibility_scenarios(test_db_session: Session, test_course: Course):
    """
    Comprehensive test of lesson accessibility scenarios
    """
    # Create a sample lesson for the test course
    sample_lesson = LessonModule(
        course_id=test_course.id,
        title="Test Lesson",
        is_visible=True,
        content_type="text",
        required_roles=["student"]
    )
    test_db_session.add(sample_lesson)
    test_db_session.commit()
    
    test_cases = [
        # Fully accessible lesson
        {
            "is_visible": True,
            "start_date": datetime.utcnow() - timedelta(days=1),
            "end_date": datetime.utcnow() + timedelta(days=30),
            "roles": ['student', 'instructor'],
            "test_roles": ['student', 'instructor'],
            "expected_results": [True, True]
        },
        # Invisible lesson
        {
            "is_visible": False,
            "start_date": datetime.utcnow() - timedelta(days=1),
            "end_date": datetime.utcnow() + timedelta(days=30),
            "roles": ['student'],
            "test_roles": ['student', 'instructor'],
            "expected_results": [False, False]
        },
        # Future lesson
        {
            "is_visible": True,
            "start_date": datetime.utcnow() + timedelta(days=1),
            "end_date": datetime.utcnow() + timedelta(days=30),
            "roles": ['student'],
            "test_roles": ['student', 'instructor'],
            "expected_results": [False, False]
        },
        # Expired lesson
        {
            "is_visible": True,
            "start_date": datetime.utcnow() - timedelta(days=30),
            "end_date": datetime.utcnow() - timedelta(days=1),
            "roles": ['student'],
            "test_roles": ['student', 'instructor'],
            "expected_results": [False, False]
        }
    ]
    
    for case in test_cases:
        # Reset lesson properties
        sample_lesson.is_visible = case["is_visible"]
        sample_lesson.visibility_start_date = case["start_date"]
        sample_lesson.visibility_end_date = case["end_date"]
        sample_lesson.required_roles = case["roles"]
        test_db_session.commit()
        
        # Test each role
        for role, expected in zip(case["test_roles"], case["expected_results"]):
            assert sample_lesson.is_accessible(role) == expected, \
                f"Failed for case: {case}, role: {role}"

def test_get_accessible_lessons(test_db_session: Session, test_course: Course):
    """
    Test retrieving accessible lessons for a course
    """
    # Create multiple lessons with different visibility settings
    now = datetime.utcnow()
    lessons = [
        LessonModule(
            course_id=test_course.id, 
            title=f"Lesson {i}", 
            is_visible=True,
            content_type="text",
            required_roles=["student"],
            visibility_start_date=now - timedelta(days=1),
            visibility_end_date=now + timedelta(days=30)
        ) for i in range(3)
    ]
    
    # Add an invisible lesson
    invisible_lesson = LessonModule(
        course_id=test_course.id,
        title="Invisible Lesson",
        is_visible=False,
        content_type="text",
        required_roles=["student"]
    )
    
    # Add a future lesson
    future_lesson = LessonModule(
        course_id=test_course.id,
        title="Future Lesson",
        is_visible=True,
        content_type="text",
        required_roles=["student"],
        visibility_start_date=now + timedelta(days=1)
    )
    
    test_db_session.add_all(lessons + [invisible_lesson, future_lesson])
    test_db_session.commit()
    
    # Retrieve accessible lessons for a student
    accessible_lessons = LessonVisibilityService.get_accessible_lessons(
        test_db_session, test_course.id, 'student'
    )
    
    assert len(accessible_lessons) == 3  # Only currently accessible lessons
    assert all(lesson.is_visible for lesson in accessible_lessons)
    assert all('student' in lesson.required_roles for lesson in accessible_lessons)

def test_lesson_role_restrictions(test_db_session: Session, test_course: Course):
    """
    Test role-based access restrictions
    """
    # Create a sample lesson for the test course
    sample_lesson = LessonModule(
        course_id=test_course.id,
        title="Test Lesson",
        is_visible=True,
        content_type="text",
        required_roles=["student"]
    )
    test_db_session.add(sample_lesson)
    test_db_session.commit()
    
    # Set lesson to only be accessible by instructors
    sample_lesson.is_visible = True
    sample_lesson.required_roles = ['instructor']
    test_db_session.commit()
    
    # Test different role scenarios
    assert sample_lesson.is_accessible('instructor') == True
    assert sample_lesson.is_accessible('student') == False
    assert sample_lesson.is_accessible('admin') == False

def test_lesson_accessibility(test_db_session: Session, test_course: Course):
    """
    Test lesson accessibility based on visibility rules
    """
    # Create a sample lesson for the test course
    sample_lesson = LessonModule(
        course_id=test_course.id,
        title="Test Lesson",
        is_visible=True,
        content_type="text",
        required_roles=["student"]
    )
    test_db_session.add(sample_lesson)
    test_db_session.commit()
    
    # Set up visibility rules
    sample_lesson.is_visible = True
    sample_lesson.visibility_start_date = datetime.utcnow() - timedelta(days=1)
    sample_lesson.visibility_end_date = datetime.utcnow() + timedelta(days=30)
    sample_lesson.required_roles = ['student']
    test_db_session.commit()
    
    # Test student role
    assert sample_lesson.is_accessible('student') == True
    
    # Test instructor role (not in required roles)
    assert sample_lesson.is_accessible('instructor') == False
    
    # Test with future start date
    sample_lesson.visibility_start_date = datetime.utcnow() + timedelta(days=1)
    test_db_session.commit()
    assert sample_lesson.is_accessible('student') == False
    
    # Test with past end date
    sample_lesson.visibility_start_date = datetime.utcnow() - timedelta(days=2)
    sample_lesson.visibility_end_date = datetime.utcnow() - timedelta(days=1)
    test_db_session.commit()
    assert sample_lesson.is_accessible('student') == False
