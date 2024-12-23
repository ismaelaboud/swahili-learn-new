import pytest
from sqlalchemy.orm import Session
from app.services.search_service import SearchService
from app.schemas.search_schema import SearchQuery

def test_course_search_basic(test_db_session, test_courses):
    """
    Test basic course search functionality
    """
    search_query = SearchQuery(text="Python")
    results = SearchService.search_courses(test_db_session, search_query)
    
    assert len(results) > 0, "Search should return results"
    for result in results:
        assert "Python" in result.title or "Python" in result.description

def test_course_search_filters(test_db_session, test_courses):
    """
    Test advanced filtering in course search
    """
    search_query = SearchQuery(
        difficulty=["beginner"],
        categories=["Web Development"],
        min_price=0,
        max_price=100
    )
    results = SearchService.search_courses(test_db_session, search_query)
    
    assert len(results) > 0, "Filtered search should return results"
    for result in results:
        assert result.difficulty == "beginner"
        assert result.price <= 100

def test_search_suggestions(test_db_session, test_courses):
    """
    Test search suggestion generation
    """
    suggestions = SearchService.get_search_suggestions(test_db_session, "Python")
    
    assert len(suggestions) > 0, "Suggestions should be generated"
    for suggestion in suggestions:
        assert "Python" in suggestion['title']

def test_search_pagination(test_db_session, test_courses):
    """
    Test search pagination
    """
    search_query_page1 = SearchQuery(page=1, page_size=5)
    search_query_page2 = SearchQuery(page=2, page_size=5)
    
    results_page1 = SearchService.search_courses(test_db_session, search_query_page1)
    results_page2 = SearchService.search_courses(test_db_session, search_query_page2)
    
    assert len(results_page1) == 5
    assert len(results_page2) == 5
    assert results_page1 != results_page2, "Different pages should have different results"
