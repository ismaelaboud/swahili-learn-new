from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.services.database import get_db
from app.services.auth import (
    get_password_hash, 
    verify_password, 
    create_access_token,
    get_current_active_user
)
from app.models.user import User
from app.schemas.user import (
    UserCreate, 
    UserResponse, 
    Token, 
    UserLogin,
    ProfileUpdate,
    PasswordResetRequest,
    PasswordResetConfirm
)
from datetime import timedelta
import os

router = APIRouter()

# Token expiration from environment
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

@router.post("/register", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=400, 
            detail="Username or email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        role=user.role
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/token", response_model=Token)
def login_for_access_token(
    user_login: UserLogin, 
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == user_login.username).first()
    
    if not user or not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get("/", response_model=List[UserResponse])
def read_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Only allow admins to list all users
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.patch("/profile", response_model=UserResponse)
def update_profile(
    profile_data: ProfileUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Check if email is already taken by another user
    if profile_data.email:
        existing_email = db.query(User).filter(
            (User.email == profile_data.email) & (User.id != current_user.id)
        ).first()
        
        if existing_email:
            raise HTTPException(
                status_code=400, 
                detail="Email already in use by another user"
            )
    
    # Update user profile
    if profile_data.full_name is not None:
        current_user.full_name = profile_data.full_name
    
    if profile_data.email is not None:
        current_user.email = profile_data.email
    
    db.commit()
    db.refresh(current_user)
    
    return current_user

@router.post("/password-reset-request")
def request_password_reset(
    reset_request: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    # Find user by email
    user = db.query(User).filter(User.email == reset_request.email).first()
    
    if not user:
        # For security, return success even if email not found
        return {"message": "If an account exists, a reset link will be sent"}
    
    # Generate reset token
    reset_token = user.generate_reset_token()
    db.commit()
    
    # TODO: In production, send an email with reset_token
    # For now, we'll return the token (only for development)
    return {
        "message": "Password reset requested",
        "reset_token": reset_token  # Remove this in production
    }

@router.post("/password-reset-confirm")
def confirm_password_reset(
    reset_data: PasswordResetConfirm,
    db: Session = Depends(get_db)
):
    # Find user by reset token
    user = db.query(User).filter(User.reset_token == reset_data.reset_token).first()
    
    if not user:
        raise HTTPException(
            status_code=400, 
            detail="Invalid or expired reset token"
        )
    
    # Validate token
    if not user.is_reset_token_valid():
        raise HTTPException(
            status_code=400, 
            detail="Reset token has expired"
        )
    
    # Update password
    user.hashed_password = get_password_hash(reset_data.new_password)
    
    # Clear reset token
    user.reset_token = None
    user.reset_token_expiration = None
    
    db.commit()
    
    return {"message": "Password successfully reset"}
