from typing import List, Optional
from pydantic import BaseModel, Field, validator

class SearchQuery(BaseModel):
    """
    Comprehensive search query model with advanced filtering
    """
    text: Optional[str] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)
    
    # Filtering options
    difficulty: Optional[List[str]] = None
    categories: Optional[List[str]] = None
    instructors: Optional[List[int]] = None
    
    # Price filtering
    min_price: Optional[float] = Field(default=None, ge=0)
    max_price: Optional[float] = Field(default=None, ge=0)
    
    # Sorting options
    sort_by: Optional[str] = Field(
        default=None, 
        pattern='^(price|rating|popularity)$'
    )
    sort_order: str = Field(default='desc', pattern='^(asc|desc)$')

    @validator('max_price')
    def validate_price_range(cls, max_price, values):
        """
        Validate that max_price is greater than min_price if both are provided
        """
        min_price = values.get('min_price')
        if min_price is not None and max_price is not None:
            if max_price < min_price:
                raise ValueError('Max price must be greater than or equal to min price')
        return max_price

class SearchResult(BaseModel):
    """
    Standardized search result model
    """
    id: int
    title: str
    description: str
    difficulty: str
    price: float
    rating: Optional[float] = None

class SearchSuggestion(BaseModel):
    """
    Search suggestion model for autocomplete
    """
    id: int
    title: str
    category: str
