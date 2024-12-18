from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List, Dict, Tuple

from app.services.database import get_db
from app.services.auth import get_current_active_user, get_current_admin_user
from app.models.user import User
from app.models.assessment import Quiz, QuizQuestion, QuizQuestionChoice, QuizSubmission, QuizSubmissionAnswer
from app.schemas.assessment import (
    QuizCreate, 
    QuizResponse, 
    QuizSubmissionCreate, 
    QuizSubmissionResponse,
    QuizSubmissionAnswerBase
)

import logging

router = APIRouter(
    prefix="/quizzes",
    tags=["quizzes"]
)

def grade_short_answer(question: QuizQuestion, user_answer: str) -> Tuple[bool, float]:
    """
    Grade a short answer question based on keywords and length
    
    Args:
        question: The quiz question with short answer criteria
        user_answer: The user's submitted answer
    
    Returns:
        A tuple of (is_correct, score)
    """
    # Default score components
    keyword_score = 0.0
    length_score = 0.0
    
    # Keyword matching
    if question.short_answer_keywords:
        # Convert both user answer and keywords to lowercase for case-insensitive matching
        user_answer_lower = user_answer.lower()
        keywords = [kw.lower() for kw in question.short_answer_keywords]
        
        # Count matched keywords
        matched_keywords = sum(1 for kw in keywords if kw in user_answer_lower)
        keyword_score = (matched_keywords / len(keywords)) * 0.6  # 60% weight to keywords
    
    # Length validation
    if question.short_answer_min_length or question.short_answer_max_length:
        answer_length = len(user_answer.strip())
        
        # Check minimum length
        if question.short_answer_min_length and answer_length < question.short_answer_min_length:
            length_score = 0.0
        # Check maximum length
        elif question.short_answer_max_length and answer_length > question.short_answer_max_length:
            length_score = 0.0
        else:
            # Normalize length score
            length_score = 0.4  # 40% weight to length
    
    # Combine scores
    total_score = keyword_score + length_score
    is_correct = total_score >= 0.5  # At least 50% to be considered correct
    
    return is_correct, total_score

@router.post("/", response_model=QuizResponse)
def create_quiz(
    quiz: QuizCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Create a new quiz for a course
    - Only admins can create quizzes
    """
    # Validate course exists
    from app.models.course import Course
    course = db.query(Course).filter(Course.id == quiz.course_id).first()
    if not course:
        logging.error(f"Course {quiz.course_id} not found")
        raise HTTPException(status_code=404, detail="Course not found")

    # Create quiz
    db_quiz = Quiz(
        course_id=quiz.course_id,
        title=quiz.title,
        description=quiz.description,
        duration_minutes=quiz.duration_minutes,
        passing_score=quiz.passing_score,
        is_timed=quiz.is_timed
    )
    db.add(db_quiz)
    db.flush()  # To get the quiz ID

    # Create questions
    for question_data in quiz.questions:
        db_question = QuizQuestion(
            quiz_id=db_quiz.id,
            question_text=question_data.question_text,
            question_type=question_data.question_type,
            points=question_data.points
        )
        db.add(db_question)
        db.flush()  # To get the question ID

        # Create choices if applicable
        if question_data.choices:
            for choice_data in question_data.choices:
                db_choice = QuizQuestionChoice(
                    question_id=db_question.id,
                    choice_text=choice_data.choice_text,
                    is_correct=choice_data.is_correct
                )
                db.add(db_choice)

    db.commit()
    db.refresh(db_quiz)
    
    return db_quiz

@router.get("/course/{course_id}", response_model=List[QuizResponse])
def get_course_quizzes(
    course_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve all quizzes for a specific course
    """
    # Validate course exists
    from app.models.course import Course
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        logging.error(f"Course {course_id} not found")
        raise HTTPException(status_code=404, detail="Course not found")

    # Get quizzes with their questions
    quizzes = db.query(Quiz).filter(Quiz.course_id == course_id).all()
    
    return quizzes

@router.post("/submit", response_model=QuizSubmissionResponse)
def submit_quiz(
    submission: QuizSubmissionCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Submit a quiz for grading with enhanced short answer support
    """
    logging.info(f"User {current_user.id} is submitting a quiz")
    logging.info(f"User details: {current_user}")

    # Validate quiz exists
    quiz = db.query(Quiz).filter(Quiz.id == submission.quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    # Create quiz submission
    db_submission = QuizSubmission(
        quiz_id=submission.quiz_id,
        user_id=current_user.id  # Explicitly set to current authenticated user
    )
    db.add(db_submission)
    db.flush()

    # Track total points and correct answers
    total_points = 0
    earned_points = 0

    # Process and grade each answer
    for answer_data in submission.answers:
        question = db.query(QuizQuestion).filter(
            QuizQuestion.id == answer_data['question_id']
        ).first()
        
        if not question:
            raise HTTPException(status_code=400, detail=f"Question {answer_data['question_id']} not found")

        # Determine correctness based on question type
        is_correct = False
        keyword_match_score = None
        length_score = None

        if question.question_type == 'multiple_choice':
            # Find the correct choice
            correct_choice = db.query(QuizQuestionChoice).filter(
                QuizQuestionChoice.question_id == question.id,
                QuizQuestionChoice.is_correct == True
            ).first()
            
            # Compare user's choice with correct choice
            is_correct = (answer_data.get('user_answer') == correct_choice.choice_text)
        
        elif question.question_type == 'true_false':
            # Find the correct choice
            correct_choice = db.query(QuizQuestionChoice).filter(
                QuizQuestionChoice.question_id == question.id,
                QuizQuestionChoice.is_correct == True
            ).first()
            
            # Compare user's choice with correct choice
            is_correct = (str(answer_data.get('user_answer')).lower() == str(correct_choice.choice_text).lower())
        
        elif question.question_type == 'short_answer':
            # Grade short answer question
            user_answer = str(answer_data.get('user_answer', '')).strip()
            is_correct, total_match_score = grade_short_answer(question, user_answer)
            
            # Detailed scoring for short answers
            keyword_match_score = total_match_score * 0.6
            length_score = total_match_score * 0.4

        # Create submission answer
        db_submission_answer = QuizSubmissionAnswer(
            submission_id=db_submission.id,
            question_id=question.id,
            user_answer=str(answer_data.get('user_answer', '')),
            is_correct=is_correct,
            keyword_match_score=keyword_match_score,
            length_score=length_score
        )
        db.add(db_submission_answer)

        # Track points
        total_points += question.points
        if is_correct:
            earned_points += question.points

    # Calculate final score and pass/fail status
    score = earned_points / total_points if total_points > 0 else 0
    is_passed = score >= quiz.passing_score

    # Update submission with final score
    db_submission.score = score
    db_submission.is_passed = is_passed

    db.commit()
    db.refresh(db_submission)

    return db_submission

@router.get("/{quiz_id}/results", response_model=QuizSubmissionResponse)
def get_quiz_submission_result(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get the latest quiz submission result for the current user
    """
    submission = db.query(QuizSubmission).filter(
        QuizSubmission.quiz_id == quiz_id,
        QuizSubmission.user_id == current_user.id
    ).order_by(QuizSubmission.submitted_at.desc()).first()

    if not submission:
        logging.error(f"No submission found for quiz {quiz_id} and user {current_user.id}")
        raise HTTPException(status_code=404, detail="No submission found")

    return submission
