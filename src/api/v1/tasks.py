from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from src.core.database import get_db
from src.schemas.task import TaskResponse, TaskCreate, TaskUpdate
from src.services.task import TaskService
from src.models.task import Task
from src.models.user import User
from src.core.auth import get_current_user


router = APIRouter()


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    创建新任务
    """
    return TaskService.create_task(db=db, task=task, creator_id=current_user.id)


@router.get("/", response_model=List[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    status: Optional[str] = Query(None),
    assignee_id: Optional[int] = Query(None),
    creator_id: Optional[int] = Query(None),
    current_user: User = Depends(get_current_user),
):
    """Get all tasks with optional filtering"""
    # Create a params dictionary with the actual query parameters
    params = {
        "status": status,
        "assignee_id": assignee_id,
        "creator_id": creator_id
    }
    
    # Filter out None values
    params = {k: v for k, v in params.items() if v is not None}
    
    # Use the task service with the filtered parameters
    tasks = TaskService.get_tasks(db, params=params)

    print(tasks)
    
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
    """
    根据ID获取任务详情
    """
    task = TaskService.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db)
):
    """Update a specific task"""
    updated_task = TaskService.update_task(db, task_id, task_update)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    删除任务
    """
    if not TaskService.delete_task(db, task_id=task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
