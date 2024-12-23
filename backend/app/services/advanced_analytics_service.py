from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc, asc
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

from app.models.user import User
from app.models.course import Course, CourseEnrollment
from app.models.assessment import Quiz, QuizSubmission, QuizSubmissionAnswer
from app.models.lesson import Lesson, LessonProgress

class AdvancedAnalyticsService:
    """
    Comprehensive performance analytics and insights generation
    """
    
    @classmethod
    def generate_learner_profile(
        cls, 
        db: Session, 
        user_id: int
    ) -> Dict[str, Any]:
        """
        Create a comprehensive learner profile with performance insights
        
        :param db: Database session
        :param user_id: User identifier
        :return: Detailed learner profile
        """
        # Basic user information
        user = db.query(User).filter(User.id == user_id).first()
        
        # Course enrollment statistics
        total_courses = db.query(CourseEnrollment).filter(
            CourseEnrollment.user_id == user_id
        ).count()
        
        completed_courses = db.query(CourseEnrollment).filter(
            CourseEnrollment.user_id == user_id,
            CourseEnrollment.status == 'completed'
        ).count()
        
        # Quiz performance
        quiz_stats = db.query(
            func.count(QuizSubmission.id).label('total_quizzes'),
            func.avg(QuizSubmission.score).label('average_score'),
            func.sum(QuizSubmission.is_passed).label('passed_quizzes')
        ).filter(
            QuizSubmission.user_id == user_id
        ).first()
        
        # Learning pace analysis
        learning_pace = db.query(
            func.avg(func.julianday(LessonProgress.completed_at) - 
                     func.julianday(LessonProgress.started_at)).label('avg_lesson_duration')
        ).filter(
            LessonProgress.user_id == user_id
        ).scalar() or 0
        
        # Skill tags and strengths
        skill_performance = cls._analyze_skill_performance(db, user_id)
        
        return {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "profile": {
                "total_courses_enrolled": total_courses,
                "completed_courses": completed_courses,
                "course_completion_rate": (completed_courses / total_courses * 100) if total_courses > 0 else 0,
                
                "quiz_performance": {
                    "total_quizzes": quiz_stats.total_quizzes,
                    "average_score": float(quiz_stats.average_score or 0),
                    "passed_quizzes": quiz_stats.passed_quizzes,
                    "pass_rate": (quiz_stats.passed_quizzes / quiz_stats.total_quizzes * 100) if quiz_stats.total_quizzes > 0 else 0
                },
                
                "learning_pace": {
                    "avg_lesson_duration_hours": learning_pace,
                    "pace_category": cls._categorize_learning_pace(learning_pace)
                },
                
                "skill_strengths": skill_performance
            }
        }
    
    @classmethod
    def _analyze_skill_performance(
        cls, 
        db: Session, 
        user_id: int
    ) -> List[Dict[str, Any]]:
        """
        Analyze user's performance across different skill domains
        
        :param db: Database session
        :param user_id: User identifier
        :return: List of skill performances
        """
        # Analyze quiz performance by lesson tags/skills
        skill_performance = db.query(
            Lesson.skill_tags,
            func.avg(QuizSubmission.score).label('avg_score'),
            func.count(QuizSubmission.id).label('total_attempts')
        ).join(
            Quiz, Quiz.lesson_id == Lesson.id
        ).join(
            QuizSubmission, QuizSubmission.quiz_id == Quiz.id
        ).filter(
            QuizSubmission.user_id == user_id
        ).group_by(
            Lesson.skill_tags
        ).order_by(
            desc('avg_score')
        ).all()
        
        return [
            {
                "skill_tag": skill_tag,
                "average_score": float(avg_score),
                "total_attempts": total_attempts,
                "proficiency_level": cls._categorize_skill_level(float(avg_score))
            } for skill_tag, avg_score, total_attempts in skill_performance
        ]
    
    @classmethod
    def _categorize_learning_pace(cls, lesson_duration: float) -> str:
        """
        Categorize learning pace based on lesson completion time
        
        :param lesson_duration: Average lesson duration in hours
        :return: Pace category
        """
        if lesson_duration < 0.5:
            return "Very Fast"
        elif lesson_duration < 1:
            return "Fast"
        elif lesson_duration < 2:
            return "Average"
        elif lesson_duration < 3:
            return "Slow"
        else:
            return "Very Slow"
    
    @classmethod
    def _categorize_skill_level(cls, score: float) -> str:
        """
        Categorize skill proficiency based on average score
        
        :param score: Average quiz score
        :return: Skill proficiency level
        """
        if score >= 0.9:
            return "Expert"
        elif score >= 0.75:
            return "Proficient"
        elif score >= 0.6:
            return "Intermediate"
        elif score >= 0.4:
            return "Beginner"
        else:
            return "Novice"
    
    @classmethod
    def generate_course_performance_visualization(
        cls, 
        db: Session, 
        course_id: int
    ) -> Dict[str, Any]:
        """
        Generate comprehensive course performance visualization
        
        :param db: Database session
        :param course_id: Course identifier
        :return: Performance visualization data
        """
        # Quiz performance distribution
        quiz_performance = db.query(
            Quiz.title,
            func.avg(QuizSubmission.score).label('avg_score'),
            func.count(QuizSubmission.id).label('total_attempts')
        ).join(
            QuizSubmission, QuizSubmission.quiz_id == Quiz.id
        ).filter(
            Quiz.course_id == course_id
        ).group_by(
            Quiz.title
        ).all()
        
        # Prepare data for visualization
        df = pd.DataFrame(
            quiz_performance, 
            columns=['Quiz', 'Average Score', 'Total Attempts']
        )
        
        # Create bar plot
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Quiz', y='Average Score', data=df)
        plt.title('Quiz Performance Distribution')
        plt.xlabel('Quiz')
        plt.ylabel('Average Score')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Save plot to buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        
        # Encode plot as base64
        plot_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plt.close()
        
        return {
            "performance_plot": plot_base64,
            "quiz_details": [
                {
                    "quiz_title": row['Quiz'],
                    "average_score": row['Average Score'],
                    "total_attempts": row['Total Attempts']
                } for _, row in df.iterrows()
            ]
        }
    
    @classmethod
    def predict_learning_outcomes(
        cls, 
        db: Session, 
        user_id: int
    ) -> Dict[str, Any]:
        """
        Predictive analytics for potential learning outcomes
        
        :param db: Database session
        :param user_id: User identifier
        :return: Predictive learning outcome insights
        """
        # Historical performance data
        performance_history = db.query(
            QuizSubmission.quiz_id,
            QuizSubmission.score,
            Quiz.difficulty_level
        ).join(
            Quiz, QuizSubmission.quiz_id == Quiz.id
        ).filter(
            QuizSubmission.user_id == user_id
        ).all()
        
        # Simple predictive model using historical performance
        difficulty_scores = {
            'beginner': 1,
            'intermediate': 2,
            'advanced': 3
        }
        
        performance_data = [
            {
                'difficulty': diff,
                'score': score,
                'difficulty_score': difficulty_scores.get(diff, 1)
            } for _, score, diff in performance_history
        ]
        
        # Basic predictive insights
        if performance_data:
            df = pd.DataFrame(performance_data)
            
            # Correlation between difficulty and performance
            correlation = df['difficulty_score'].corr(df['score'])
            
            # Predicted future performance
            predicted_performance = df['score'].mean() + (correlation * 0.1)
            
            return {
                "historical_performance": {
                    "average_score": df['score'].mean(),
                    "performance_variance": df['score'].std()
                },
                "predictive_insights": {
                    "difficulty_performance_correlation": correlation,
                    "predicted_future_performance": predicted_performance,
                    "recommended_difficulty": (
                        'advanced' if predicted_performance > 0.8 else
                        'intermediate' if predicted_performance > 0.6 else
                        'beginner'
                    )
                }
            }
        
        return {
            "message": "Insufficient data for predictive analysis"
        }
