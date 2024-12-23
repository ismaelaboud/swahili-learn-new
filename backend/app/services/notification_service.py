from typing import Dict, List, Optional, Union
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.models.user import User
from app.models.course import Course, CourseEnrollment
from app.models.assessment import Quiz, QuizSubmission
from app.core.config import settings

class NotificationService:
    """
    Comprehensive notification system for Swahili Learn
    Supports email, in-app, and potential future notification channels
    """
    
    @classmethod
    def send_email(
        cls, 
        to_email: str, 
        subject: str, 
        body: str, 
        html_body: Optional[str] = None
    ) -> bool:
        """
        Send an email notification
        
        :param to_email: Recipient email address
        :param subject: Email subject
        :param body: Plain text email body
        :param html_body: Optional HTML version of the email
        :return: Whether email was sent successfully
        """
        try:
            # Create message container
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = settings.EMAIL_FROM
            msg['To'] = to_email
            
            # Plain text part
            msg.attach(MIMEText(body, 'plain'))
            
            # HTML part (if provided)
            if html_body:
                msg.attach(MIMEText(html_body, 'html'))
            
            # Send email
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                server.sendmail(settings.EMAIL_FROM, to_email, msg.as_string())
            
            return True
        except Exception as e:
            # Log the error (you'd typically use a proper logging system)
            print(f"Email sending failed: {e}")
            return False
    
    @classmethod
    def create_in_app_notification(
        cls, 
        db: Session, 
        user_id: int, 
        message: str, 
        notification_type: str,
        related_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create an in-app notification
        
        :param db: Database session
        :param user_id: User to notify
        :param message: Notification message
        :param notification_type: Type of notification
        :param related_id: Optional ID of related entity
        :return: Created notification details
        """
        from app.models.notification import Notification
        
        notification = Notification(
            user_id=user_id,
            message=message,
            type=notification_type,
            related_id=related_id,
            is_read=False,
            created_at=datetime.utcnow()
        )
        
        db.add(notification)
        db.commit()
        db.refresh(notification)
        
        return {
            "id": notification.id,
            "message": notification.message,
            "type": notification.type
        }
    
    @classmethod
    def send_course_enrollment_notification(
        cls, 
        db: Session, 
        user: User, 
        course: Course
    ) -> None:
        """
        Send notifications for course enrollment
        
        :param db: Database session
        :param user: Enrolled user
        :param course: Enrolled course
        """
        # Email notification
        email_subject = f"Enrolled in {course.title}"
        email_body = f"""
        Hello {user.username},
        
        You have successfully enrolled in the course: {course.title}
        
        Course Description: {course.description}
        Start Date: {course.start_date}
        
        Get ready to start learning!
        
        Best regards,
        Swahili Learn Team
        """
        
        # Send email
        cls.send_email(
            to_email=user.email, 
            subject=email_subject, 
            body=email_body
        )
        
        # In-app notification
        cls.create_in_app_notification(
            db=db,
            user_id=user.id,
            message=f"You've enrolled in {course.title}",
            notification_type="course_enrollment",
            related_id=course.id
        )
    
    @classmethod
    def send_quiz_deadline_reminders(
        cls, 
        db: Session
    ) -> List[Dict[str, Any]]:
        """
        Send quiz deadline reminders
        
        :param db: Database session
        :return: List of sent reminders
        """
        # Find upcoming quizzes within next 48 hours
        now = datetime.utcnow()
        deadline = now + timedelta(hours=48)
        
        # Find quizzes and their enrolled students
        upcoming_quizzes = db.query(Quiz, CourseEnrollment, User).join(
            CourseEnrollment, CourseEnrollment.course_id == Quiz.course_id
        ).join(
            User, User.id == CourseEnrollment.user_id
        ).filter(
            Quiz.is_timed == True,
            Quiz.duration_minutes is not None
        ).all()
        
        sent_reminders = []
        
        for quiz, enrollment, user in upcoming_quizzes:
            # Check if user hasn't submitted the quiz
            existing_submission = db.query(QuizSubmission).filter(
                QuizSubmission.quiz_id == quiz.id,
                QuizSubmission.user_id == user.id
            ).first()
            
            if not existing_submission:
                # Send reminder
                reminder_email = f"""
                Upcoming Quiz Deadline: {quiz.title}
                
                You have an upcoming quiz that needs to be completed:
                Course: {quiz.course.title}
                Quiz: {quiz.title}
                Duration: {quiz.duration_minutes} minutes
                
                Don't miss out! Log in and complete the quiz soon.
                
                Best regards,
                Swahili Learn Team
                """
                
                # Send email and in-app notification
                email_sent = cls.send_email(
                    to_email=user.email,
                    subject=f"Upcoming Quiz: {quiz.title}",
                    body=reminder_email
                )
                
                in_app_notification = cls.create_in_app_notification(
                    db=db,
                    user_id=user.id,
                    message=f"Reminder: Quiz '{quiz.title}' is coming up",
                    notification_type="quiz_reminder",
                    related_id=quiz.id
                )
                
                sent_reminders.append({
                    "user_email": user.email,
                    "quiz_title": quiz.title,
                    "email_sent": email_sent
                })
        
        db.commit()
        return sent_reminders
    
    @classmethod
    def mark_notifications_as_read(
        cls, 
        db: Session, 
        user_id: int, 
        notification_ids: Optional[List[int]] = None
    ) -> int:
        """
        Mark notifications as read
        
        :param db: Database session
        :param user_id: User whose notifications to mark
        :param notification_ids: Optional list of specific notification IDs
        :return: Number of notifications marked as read
        """
        from app.models.notification import Notification
        
        query = db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        )
        
        if notification_ids:
            query = query.filter(Notification.id.in_(notification_ids))
        
        updated_count = query.update(
            {"is_read": True}, 
            synchronize_session=False
        )
        
        db.commit()
        return updated_count
