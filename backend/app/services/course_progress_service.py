from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime
import uuid
import qrcode
import io
import base64
from PIL import Image, ImageDraw, ImageFont

from app.models.user import User
from app.models.course import Course, CourseEnrollment, CourseModule, CourseLesson
from app.models.assessment import Quiz, QuizSubmission
from app.core.config import settings

class CourseProgressService:
    """
    Comprehensive course progress tracking and certificate generation service
    """
    
    @classmethod
    def calculate_course_progress(
        cls, 
        db: Session, 
        user_id: int, 
        course_id: int
    ) -> Dict[str, Any]:
        """
        Calculate detailed course progress for a user
        
        :param db: Database session
        :param user_id: User identifier
        :param course_id: Course identifier
        :return: Detailed progress dictionary
        """
        # Total modules and lessons in the course
        total_modules = db.query(CourseModule).filter(
            CourseModule.course_id == course_id
        ).count()
        
        total_lessons = db.query(CourseLesson).filter(
            CourseLesson.course_id == course_id
        ).count()
        
        # Completed lessons
        completed_lessons = db.query(CourseLesson).join(
            QuizSubmission, 
            and_(
                QuizSubmission.quiz_id == CourseLesson.quiz_id,
                QuizSubmission.user_id == user_id,
                QuizSubmission.is_passed == True
            )
        ).filter(
            CourseLesson.course_id == course_id
        ).count()
        
        # Quiz performance
        quiz_performance = db.query(
            func.avg(QuizSubmission.score)
        ).join(
            CourseLesson,
            CourseLesson.quiz_id == QuizSubmission.quiz_id
        ).filter(
            CourseLesson.course_id == course_id,
            QuizSubmission.user_id == user_id
        ).scalar() or 0
        
        # Progress calculations
        lesson_progress = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
        module_progress = (completed_lessons / total_lessons * total_modules) if total_lessons > 0 else 0
        
        return {
            "total_modules": total_modules,
            "total_lessons": total_lessons,
            "completed_lessons": completed_lessons,
            "lesson_progress_percentage": lesson_progress,
            "module_progress_percentage": module_progress,
            "average_quiz_score": quiz_performance,
            "is_course_completed": lesson_progress >= 100
        }
    
    @classmethod
    def generate_course_certificate(
        cls, 
        db: Session, 
        user_id: int, 
        course_id: int
    ) -> Dict[str, Any]:
        """
        Generate a course completion certificate
        
        :param db: Database session
        :param user_id: User identifier
        :param course_id: Course identifier
        :return: Certificate details
        """
        # Verify course completion
        progress = cls.calculate_course_progress(db, user_id, course_id)
        
        if not progress['is_course_completed']:
            return {
                "error": "Course not completed",
                "progress": progress
            }
        
        # Fetch user and course details
        user = db.query(User).filter(User.id == user_id).first()
        course = db.query(Course).filter(Course.id == course_id).first()
        
        if not user or not course:
            raise ValueError("User or Course not found")
        
        # Generate unique certificate ID
        certificate_id = str(uuid.uuid4())
        
        # Generate QR Code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(f"{settings.BASE_URL}/verify-certificate/{certificate_id}")
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Create certificate image
        certificate = Image.new('RGB', (1200, 800), color='white')
        draw = ImageDraw.Draw(certificate)
        
        # Load fonts
        title_font = ImageFont.truetype("path/to/fonts/Montserrat-Bold.ttf", 60)
        subtitle_font = ImageFont.truetype("path/to/fonts/Montserrat-Regular.ttf", 40)
        details_font = ImageFont.truetype("path/to/fonts/Montserrat-Light.ttf", 30)
        
        # Draw certificate elements
        draw.text((600, 200), "Certificate of Completion", font=title_font, fill='black', anchor='mm')
        draw.text((600, 300), f"This is to certify that", font=subtitle_font, fill='black', anchor='mm')
        draw.text((600, 400), user.username, font=title_font, fill='black', anchor='mm')
        draw.text((600, 500), f"has successfully completed the course", font=subtitle_font, fill='black', anchor='mm')
        draw.text((600, 550), course.title, font=title_font, fill='black', anchor='mm')
        
        # Add completion details
        draw.text((200, 700), f"Completion Date: {datetime.utcnow().strftime('%Y-%m-%d')}", font=details_font, fill='black')
        draw.text((900, 700), f"Certificate ID: {certificate_id}", font=details_font, fill='black')
        
        # Embed QR Code
        qr_resized = qr_img.resize((200, 200))
        certificate.paste(qr_resized, (50, 50))
        
        # Save certificate
        certificate_buffer = io.BytesIO()
        certificate.save(certificate_buffer, format='PNG')
        certificate_base64 = base64.b64encode(certificate_buffer.getvalue()).decode('utf-8')
        
        # Store certificate in database
        from app.models.certificate import Certificate
        
        certificate_record = Certificate(
            user_id=user_id,
            course_id=course_id,
            certificate_id=certificate_id,
            issued_at=datetime.utcnow()
        )
        
        db.add(certificate_record)
        db.commit()
        
        return {
            "certificate_id": certificate_id,
            "user_id": user_id,
            "course_id": course_id,
            "course_title": course.title,
            "certificate_image": certificate_base64,
            "verification_url": f"{settings.BASE_URL}/verify-certificate/{certificate_id}"
        }
    
    @classmethod
    def verify_certificate(
        cls, 
        db: Session, 
        certificate_id: str
    ) -> Dict[str, Any]:
        """
        Verify a course completion certificate
        
        :param db: Database session
        :param certificate_id: Certificate identifier
        :return: Certificate verification details
        """
        from app.models.certificate import Certificate
        
        certificate = db.query(Certificate).filter(
            Certificate.certificate_id == certificate_id
        ).first()
        
        if not certificate:
            return {
                "is_valid": False,
                "message": "Certificate not found"
            }
        
        return {
            "is_valid": True,
            "user_id": certificate.user_id,
            "course_id": certificate.course_id,
            "issued_at": certificate.issued_at,
            "course_title": certificate.course.title,
            "user_name": certificate.user.username
        }
