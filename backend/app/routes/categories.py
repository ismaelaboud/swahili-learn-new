from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.services.database import get_db
from app.services.auth import get_current_active_user
from app.models.user import User
from app.models.course import Category
from app.schemas.course import CategoryCreate, CategoryResponse

router = APIRouter()

@router.post("/", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Only admins can create categories
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to create categories")
    
    # Check if category already exists
    existing_category = db.query(Category).filter(Category.name == category.name).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category already exists")
    
    # Create new category
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category

@router.get("/", response_model=List[CategoryResponse])
def list_categories(
    db: Session = Depends(get_db)
):
    categories = db.query(Category).all()
    return categories

@router.delete("/{category_id}", response_model=dict)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Only admins can delete categories
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete categories")
    
    # Find the category
    db_category = db.query(Category).filter(Category.id == category_id).first()
    
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if category is in use
    if db_category.courses:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete category with existing courses"
        )
    
    # Delete category
    db.delete(db_category)
    db.commit()
    
    return {"message": "Category successfully deleted"}
