from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Union
from datetime import datetime
from enum import Enum

class QuestionTypeEnum(str, Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"

class QuizQuestionChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool = False

class QuizQuestionChoiceCreate(QuizQuestionChoiceBase):
    pass

class QuizQuestionChoiceResponse(QuizQuestionChoiceBase):
    id: int

class QuizQuestionBase(BaseModel):
    question_text: str
    question_type: str  # multiple_choice, true_false, short_answer
    points: float = 1.0

class QuizQuestionCreate(QuizQuestionBase):
    short_answer_keywords: Optional[List[str]] = None
    short_answer_min_length: Optional[int] = None
    short_answer_max_length: Optional[int] = None
    choices: Optional[List[QuizQuestionChoiceCreate]] = None

class QuizQuestionResponse(QuizQuestionBase):
    id: int
    quiz_id: int
    short_answer_keywords: Optional[List[str]] = None
    short_answer_min_length: Optional[int] = None
    short_answer_max_length: Optional[int] = None
    choices: Optional[List[QuizQuestionChoiceResponse]] = None

    model_config = ConfigDict(from_attributes=True)

class QuizBase(BaseModel):
    course_id: int
    title: str
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    passing_score: float = 0.7
    is_timed: bool = False

class QuizCreate(QuizBase):
    questions: List[QuizQuestionCreate]

class QuizResponse(QuizBase):
    id: int
    created_at: datetime
    questions: List[QuizQuestionResponse]

    model_config = ConfigDict(from_attributes=True)

class QuizSubmissionBase(BaseModel):
    quiz_id: int

class QuizSubmissionCreate(QuizSubmissionBase):
    user_id: int
    answers: List[dict]  # Flexible schema for different question types

class QuizSubmissionResponse(QuizSubmissionBase):
    id: int
    score: Optional[float]
    is_passed: bool
    submitted_at: datetime
    user_id: int

    model_config = ConfigDict(from_attributes=True)

class QuizSubmissionAnswerBase(BaseModel):
    question_id: int
    user_answer: str

class QuizSubmissionAnswerCreate(QuizSubmissionAnswerBase):
    pass

class QuizSubmissionAnswerResponse(QuizSubmissionAnswerBase):
    id: int
    is_correct: bool
    keyword_match_score: Optional[float] = None
    length_score: Optional[float] = None
    manual_score: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)
