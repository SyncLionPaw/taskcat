from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = None
    progress: Optional[float] = None
    difficulty: Optional[int] = 1
    points: Optional[int] = 0


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    progress: Optional[float] = None
    assignee_id: Optional[int] = None
    difficulty: Optional[int] = None
    points: Optional[int] = None


class TaskResponse(TaskBase):
    id: int
    creator_id: int
    assignee_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    difficulty: Optional[int] = 1
    points: Optional[int] = 0

    class Config:
        orm_mode = True
        from_attributes = True  # Add this for newer Pydantic versions
