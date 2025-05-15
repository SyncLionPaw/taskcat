from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "pending"
    progress: Optional[float] = 0.0  # Add progress field with default value

class TaskCreate(TaskBase):
    assignee_id: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    progress: Optional[float] = None  # Add progress field to update schema
    creator_id: Optional[int] = None
    assignee_id: Optional[int] = None

class TaskResponse(TaskBase):
    id: int
    creator_id: Optional[int] = None
    assignee_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True