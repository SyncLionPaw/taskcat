from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    username: str
    # Remove is_active and is_superuser fields


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    # Remove is_active and is_superuser fields


class User(UserBase):
    id: int
    created_at: datetime
    # Make updated_at optional to handle None values
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class UserResponse(User):
    """Response model for user data to be returned via the API"""
    pass


class UserInDB(User):
    hashed_password: str