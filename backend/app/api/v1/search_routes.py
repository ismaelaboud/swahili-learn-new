from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.services.search_service import SearchService
from app.schemas.search_schema import SearchQuery, SearchResult, SearchSuggestion
from app.core.security import get_current_user

router = APIRouter(prefix="/search", tags=["Search"])

@router.post("/courses", response_model=List[SearchResult])
async def search_courses(
    search_query: SearchQuery,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Advanced course search endpoint with comprehensive filtering
    
    :param search_query: Search parameters
    :param db: Database session
    :param current_user: Authenticated user
    :return: List of matching courses
    """
    return SearchService.search_courses(db, search_query)

@router.get("/suggestions", response_model=List[SearchSuggestion])
async def get_search_suggestions(
    text: str = Query(..., min_length=2, max_length=50),
    limit: Optional[int] = Query(default=5, ge=1, le=10),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Generate search suggestions based on partial text
    
    :param text: Partial search text
    :param limit: Maximum number of suggestions
    :param db: Database session
    :param current_user: Authenticated user
    :return: List of search suggestions
    """
    return SearchService.get_search_suggestions(db, text, limit)
