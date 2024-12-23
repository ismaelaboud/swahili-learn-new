from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from sqlalchemy.sql import func

from app.models.course import Course
from app.schemas.search_schema import SearchQuery, SearchResult
from app.exceptions import SearchException

class SearchService:
    """
    Comprehensive search service for courses and lesson modules
    Supports advanced filtering and ranking
    """

    @staticmethod
    def search_courses(
        db: Session, 
        query: SearchQuery
    ) -> List[SearchResult]:
        """
        Advanced course search with multiple filtering options
        
        :param db: Database session
        :param query: Search query parameters
        :return: List of search results
        """
        try:
            # Base query
            search_query = db.query(Course)

            # Text search across multiple fields
            if query.text:
                text_filter = or_(
                    Course.title.ilike(f"%{query.text}%"),
                    Course.description.ilike(f"%{query.text}%"),
                    Course.tags.ilike(f"%{query.text}%")
                )
                search_query = search_query.filter(text_filter)

            # Difficulty level filtering
            if query.difficulty:
                search_query = search_query.filter(
                    Course.difficulty_level.in_(query.difficulty)
                )

            # Category filtering
            if query.categories:
                search_query = search_query.filter(
                    Course.category.in_(query.categories)
                )

            # Instructor filtering
            if query.instructors:
                search_query = search_query.filter(
                    Course.instructor_id.in_(query.instructors)
                )

            # Price range filtering
            if query.min_price is not None:
                search_query = search_query.filter(
                    Course.price >= query.min_price
                )
            if query.max_price is not None:
                search_query = search_query.filter(
                    Course.price <= query.max_price
                )

            # Sorting
            if query.sort_by:
                sort_mapping = {
                    'price': Course.price,
                    'rating': Course.average_rating,
                    'popularity': Course.total_enrollments
                }
                sort_column = sort_mapping.get(query.sort_by)
                if sort_column:
                    search_query = search_query.order_by(
                        sort_column.desc() if query.sort_order == 'desc' else sort_column.asc()
                    )

            # Pagination
            search_query = search_query.offset(
                (query.page - 1) * query.page_size
            ).limit(query.page_size)

            # Execute and transform results
            results = search_query.all()
            return [
                SearchResult(
                    id=course.id,
                    title=course.title,
                    description=course.description,
                    difficulty=course.difficulty_level,
                    price=course.price,
                    rating=course.average_rating
                ) for course in results
            ]

        except Exception as e:
            raise SearchException(f"Search failed: {str(e)}")

    @staticmethod
    def get_search_suggestions(
        db: Session, 
        text: str, 
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate search suggestions based on partial text
        
        :param db: Database session
        :param text: Partial search text
        :param limit: Maximum number of suggestions
        :return: List of suggestion dictionaries
        """
        try:
            suggestions = db.query(Course).filter(
                or_(
                    Course.title.ilike(f"%{text}%"),
                    Course.tags.ilike(f"%{text}%")
                )
            ).limit(limit).all()

            return [
                {
                    'id': course.id,
                    'title': course.title,
                    'category': course.category
                } for course in suggestions
            ]

        except Exception as e:
            raise SearchException(f"Suggestions retrieval failed: {str(e)}")
