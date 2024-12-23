from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.assessment import Quiz, QuizSubmission, QuizSubmissionAnswer, QuizQuestion
from app.models.user import User
from app.schemas.quiz_schemas import QuizSubmissionCreate
from app.core.exceptions import QuizTimeoutException, QuizValidationError

class QuizService:
    """
    Service for managing quiz submissions and timed assessments
    """
    
    @classmethod
    def start_quiz(
        cls, 
        db: Session, 
        quiz_id: int, 
        user_id: int
    ) -> Dict[str, Any]:
        """
        Initiate a quiz attempt with time tracking
        
        :param db: Database session
        :param quiz_id: Quiz identifier
        :param user_id: User attempting the quiz
        :return: Quiz start information
        """
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            raise QuizValidationError("Quiz not found")
        
        # Check if quiz is timed
        if quiz.is_timed and quiz.duration_minutes:
            start_time = datetime.utcnow()
            end_time = start_time + timedelta(minutes=quiz.duration_minutes)
            
            # Create quiz submission with start and end times
            submission = QuizSubmission(
                quiz_id=quiz_id,
                user_id=user_id,
                submitted_at=start_time,
                time_limit_end=end_time
            )
            db.add(submission)
            db.commit()
            db.refresh(submission)
            
            return {
                "submission_id": submission.id,
                "start_time": start_time,
                "end_time": end_time,
                "duration_minutes": quiz.duration_minutes
            }
        else:
            # For untimed quizzes, create a standard submission
            submission = QuizSubmission(
                quiz_id=quiz_id,
                user_id=user_id
            )
            db.add(submission)
            db.commit()
            db.refresh(submission)
            
            return {
                "submission_id": submission.id,
                "is_timed": False
            }
    
    @classmethod
    def submit_quiz(
        cls, 
        db: Session, 
        submission_id: int, 
        answers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Submit quiz answers with time validation and grading
        
        :param db: Database session
        :param submission_id: Quiz submission identifier
        :param answers: List of user's answers
        :return: Quiz submission result
        """
        submission = db.query(QuizSubmission).filter(
            QuizSubmission.id == submission_id
        ).first()
        
        if not submission:
            raise QuizValidationError("Submission not found")
        
        # Time validation for timed quizzes
        if submission.time_limit_end:
            current_time = datetime.utcnow()
            if current_time > submission.time_limit_end:
                raise QuizTimeoutException("Quiz time has expired")
        
        # Process and grade each answer
        total_score = 0
        max_possible_score = 0
        submission_answers = []
        
        for answer_data in answers:
            question = db.query(QuizQuestion).filter(
                QuizQuestion.id == answer_data['question_id']
            ).first()
            
            if not question:
                continue
            
            max_possible_score += question.points
            
            # Grade the answer based on question type
            is_correct, score = cls._grade_answer(
                question, 
                answer_data['user_answer']
            )
            
            total_score += score
            
            submission_answer = QuizSubmissionAnswer(
                submission_id=submission_id,
                question_id=question.id,
                user_answer=answer_data['user_answer'],
                is_correct=is_correct,
                manual_score=score
            )
            submission_answers.append(submission_answer)
        
        # Add answers to database
        db.add_all(submission_answers)
        
        # Update submission with final score
        submission.score = total_score / max_possible_score if max_possible_score > 0 else 0
        submission.is_passed = submission.score >= submission.quiz.passing_score
        
        db.commit()
        
        return {
            "submission_id": submission.id,
            "score": submission.score,
            "passed": submission.is_passed,
            "total_questions": len(answers),
            "correct_answers": sum(1 for ans in submission_answers if ans.is_correct)
        }
    
    @classmethod
    def _grade_answer(
        cls, 
        question: QuizQuestion, 
        user_answer: str
    ) -> tuple[bool, float]:
        """
        Grade an individual answer based on question type
        
        :param question: Quiz question object
        :param user_answer: User's submitted answer
        :return: Tuple of (is_correct, score)
        """
        if question.question_type == 'multiple_choice':
            # Find the correct choice
            correct_choice = next(
                (choice for choice in question.choices if choice.is_correct), 
                None
            )
            return (
                user_answer == str(correct_choice.id), 
                question.points if user_answer == str(correct_choice.id) else 0
            )
        
        elif question.question_type == 'true_false':
            return (
                user_answer.lower() == 'true', 
                question.points if user_answer.lower() == 'true' else 0
            )
        
        elif question.question_type == 'short_answer':
            # Basic keyword matching and length validation
            keywords = question.short_answer_keywords or []
            min_length = question.short_answer_min_length or 0
            max_length = question.short_answer_max_length or float('inf')
            
            # Check length
            if len(user_answer) < min_length or len(user_answer) > max_length:
                return False, 0
            
            # Check keywords
            keyword_matches = sum(
                keyword.lower() in user_answer.lower() 
                for keyword in keywords
            )
            
            is_correct = keyword_matches > 0
            score = (keyword_matches / len(keywords)) * question.points
            
            return is_correct, score
        
        return False, 0
