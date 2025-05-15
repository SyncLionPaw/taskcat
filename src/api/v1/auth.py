from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Dict

from src.core.database import get_db
from src.core.security import create_access_token
from src.core.auth import authenticate_user, get_current_user
from src.models.user import User

# Create router without prefix - will be added in main.py
router = APIRouter()

# Increase token expiration time for better user experience
ACCESS_TOKEN_EXPIRE_MINUTES = 60

@router.post("/login")
def login(
    credentials: Dict[str, str] = Body(...),
    db: Session = Depends(get_db)
):
    """
    Simple login endpoint that accepts JSON credentials and returns user and token
    to match frontend expectations
    """
    username = credentials.get("username")
    password = credentials.get("password")
    
    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and password are required",
        )
    
    user = authenticate_user(db, username=username, password=password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # Format user data to match frontend expectations, handle missing fields
    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_active": getattr(user, "is_active", True),  # Default to True if field doesn't exist
        "is_superuser": getattr(user, "is_superuser", False)  # Default to False if field doesn't exist
    }
    
    # Return format: { user: {...}, token: "..." }
    return {
        "user": user_data,
        "token": access_token
    }

@router.post("/logout")
def logout():
    """
    Logout endpoint - frontend will handle token removal
    """
    return {"message": "Successfully logged out"}

@router.get("/me")
async def read_current_user(current_user: User = Depends(get_current_user)):
    """
    Get current user endpoint
    """
    # Return user data without wrapping to match frontend expectations
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "is_active": getattr(current_user, "is_active", True),  # Default to True if field doesn't exist
        "is_superuser": getattr(current_user, "is_superuser", False)  # Default to False if field doesn't exist
    }
