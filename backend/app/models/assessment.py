from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, Float, Enum, JSON
from sqlalchemy.orm import relationship
from app.services.database import Base
from datetime import datetime
from enum import Enum as PyEnum

class QuestionType(str, PyEnum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"

class Quiz(Base):
    """
    Represents a quiz associated with a course or lesson
    """
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    duration_minutes = Column(Integer, nullable=True)  # Optional time limit
    passing_score = Column(Float, default=0.7)  # 70% default passing score
    is_timed = Column(Boolean, default=False)
    
    # Relationships
    course = relationship("Course", back_populates="quizzes")
    questions = relationship("QuizQuestion", back_populates="quiz", cascade="all, delete-orphan")
    submissions = relationship("QuizSubmission", back_populates="quiz")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class QuizQuestion(Base):
    """
    Represents individual questions within a quiz
    """
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'), nullable=False)
    question_text = Column(String, nullable=False)
    question_type = Column(String, nullable=False)  # multiple_choice, true_false, short_answer
    points = Column(Float, default=1.0)
    
    # Add a field for short answer grading criteria
    short_answer_keywords = Column(JSON, nullable=True)  # Store keywords for basic grading
    short_answer_min_length = Column(Integer, nullable=True)  # Minimum expected answer length
    short_answer_max_length = Column(Integer, nullable=True)  # Maximum allowed answer length

    # Relationships
    quiz = relationship("Quiz", back_populates="questions")
    choices = relationship("QuizQuestionChoice", back_populates="question", cascade="all, delete-orphan")
    submission_answers = relationship("QuizSubmissionAnswer", back_populates="question")

class QuizQuestionChoice(Base):
    """
    Represents multiple choice options for quiz questions
    """
    __tablename__ = "quiz_question_choices"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey('quiz_questions.id'), nullable=False)
    choice_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)
    
    # Relationship
    question = relationship("QuizQuestion", back_populates="choices")

class QuizSubmission(Base):
    """
    Represents a student's submission of a quiz
    """
    __tablename__ = "quiz_submissions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    score = Column(Float, nullable=True)
    is_passed = Column(Boolean, default=False)
    
    # Relationships
    quiz = relationship("Quiz", back_populates="submissions")
    user = relationship("User")
    submission_answers = relationship("QuizSubmissionAnswer", back_populates="submission")
    
    submitted_at = Column(DateTime, default=datetime.utcnow)

class QuizSubmissionAnswer(Base):
    """
    Represents a student's answer to a specific quiz question
    """
    __tablename__ = "quiz_submission_answers"

    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey('quiz_submissions.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('quiz_questions.id'), nullable=False)
    user_answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)
    
    # Additional fields for short answer grading details
    keyword_match_score = Column(Float, nullable=True)  # Percentage of keywords matched
    length_score = Column(Float, nullable=True)  # Score based on answer length
    manual_score = Column(Float, nullable=True)  # Optional manual grading score

    # Relationships
    submission = relationship("QuizSubmission", back_populates="submission_answers")
    question = relationship("QuizQuestion", back_populates="submission_answers")
