from typing import Dict, List, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_

from app.models.user import User
from app.models.assessment import Quiz, QuizSubmission, QuizSubmissionAnswer
from app.models.course import Course, CourseEnrollment

class PerformanceAnalytics:
    """
    Comprehensive performance tracking and analytics service
    """
    
    @classmethod
    def get_user_quiz_performance(
        cls, 
        db: Session, 
        user_id: int, 
        course_id: int = None
    ) -> Dict[str, Any]:
        """
        Get detailed quiz performance for a user
        
        :param db: Database session
        :param user_id: User's ID
        :param course_id: Optional course filter
        :return: Performance analytics dictionary
        """
        # Total quizzes taken
        query = db.query(
            Quiz, 
            QuizSubmission
        ).join(
            QuizSubmission, 
            and_(
                QuizSubmission.quiz_id == Quiz.id, 
                QuizSubmission.user_id == user_id
            )
        )
        
        if course_id:
            query = query.filter(Quiz.course_id == course_id)
        
        quiz_submissions = query.all()
        
        analytics = {
            'total_quizzes': len(quiz_submissions),
            'passed_quizzes': 0,
            'average_score': 0.0,
            'quiz_performances': []
        }
        
        total_score = 0
        for quiz, submission in quiz_submissions:
            if submission.is_passed:
                analytics['passed_quizzes'] += 1
            
            total_score += submission.score
            
            analytics['quiz_performances'].append({
                'quiz_id': quiz.id,
                'quiz_title': quiz.title,
                'score': submission.score,
                'passed': submission.is_passed,
                'submitted_at': submission.submitted_at
            })
        
        # Calculate average score
        if analytics['total_quizzes'] > 0:
            analytics['average_score'] = total_score / analytics['total_quizzes']
        
        return analytics
    
    @classmethod
    def get_course_performance_summary(
        cls, 
        db: Session, 
        course_id: int
    ) -> Dict[str, Any]:
        """
        Get comprehensive performance summary for a course
        
        :param db: Database session
        :param course_id: Course ID
        :return: Course performance summary
        """
        # Total enrolled students
        total_students = db.query(CourseEnrollment).filter(
            CourseEnrollment.course_id == course_id
        ).count()
        
        # Quiz performance
        quiz_performance = db.query(
            Quiz.id, 
            Quiz.title,
            func.avg(QuizSubmission.score).label('avg_score'),
            func.count(QuizSubmission.id).label('total_attempts'),
            func.sum(QuizSubmission.is_passed).label('passed_attempts')
        ).join(
            QuizSubmission, 
            QuizSubmission.quiz_id == Quiz.id
        ).filter(
            Quiz.course_id == course_id
        ).group_by(
            Quiz.id, Quiz.title
        ).all()
        
        summary = {
            'total_students': total_students,
            'quizzes': []
        }
        
        for quiz_id, title, avg_score, total_attempts, passed_attempts in quiz_performance:
            summary['quizzes'].append({
                'quiz_id': quiz_id,
                'title': title,
                'average_score': float(avg_score) if avg_score else 0.0,
                'total_attempts': total_attempts,
                'pass_rate': (passed_attempts / total_attempts) * 100 if total_attempts > 0 else 0
            })
        
        return summary
    
    @classmethod
    def identify_learning_gaps(
        cls, 
        db: Session, 
        user_id: int
    ) -> List[Dict[str, Any]]:
        """
        Identify areas where a student needs improvement
        
        :param db: Database session
        :param user_id: User's ID
        :return: List of learning gaps
        """
        # Analyze incorrect answers
        learning_gaps = db.query(
            QuizQuestion.question_text,
            func.count(QuizSubmissionAnswer.id).label('incorrect_count')
        ).join(
            QuizSubmissionAnswer, 
            and_(
                QuizSubmissionAnswer.question_id == QuizQuestion.id,
                QuizSubmissionAnswer.is_correct == False
            )
        ).join(
            QuizSubmission,
            QuizSubmission.id == QuizSubmissionAnswer.submission_id
        ).filter(
            QuizSubmission.user_id == user_id
        ).group_by(
            QuizQuestion.question_text
        ).order_by(
            func.count(QuizSubmissionAnswer.id).desc()
        ).limit(5).all()
        
        return [
            {
                'question': question,
                'incorrect_attempts': count
            } for question, count in learning_gaps
        ]
