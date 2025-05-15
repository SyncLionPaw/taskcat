from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import timedelta

from src.core.database import get_db
from src.core.security import create_access_token, verify_password
from src.schemas.token import Token
from src.schemas.user import UserResponse
from src.services.user import UserService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = UserService.authenticate_user(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
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


@router.post("/logout")
def logout():
    """
    Logout endpoint - frontend will handle token removal
    """
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: UserResponse = Depends(UserService.get_current_user)):
    """
    Get current user
    """
    return current_user
