from pydantic import BaseModel, StringConstraints, Field
from typing import Annotated
from datetime import datetime
from typing import Optional
from .user import UserResponse

# Define custom string types with constraints
TaskTitle = Annotated[
    str, 
    StringConstraints(
        min_length=1,
        max_length=100,
        strip_whitespace=True
    )
]

TaskStatus = Annotated[
    str,
    StringConstraints(
        pattern='^(pending|in_progress|completed)$'
    )
]

class TaskBase(BaseModel):
    title: TaskTitle
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    status: TaskStatus = "pending"
    progress: float = Field(default=0.0, ge=0.0, le=100.0)  # Add progress field with validation

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: Optional[TaskTitle] = None
    status: Optional[TaskStatus] = None

class TaskResponse(TaskBase):
    id: int
    creator_id: int
    progress: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    creator: Optional[UserResponse] = None
    assignee: Optional[UserResponse] = None

    class Config:
        from_attributes = True