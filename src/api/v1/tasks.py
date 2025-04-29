from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from src.core.database import get_db
from src.schemas.task import TaskResponse, TaskCreate, TaskUpdate
from src.services.task import TaskService

router = APIRouter()


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    # TODO: 后续添加认证后，从token中获取用户ID
    current_user_id: int = 1,
):
    """
    创建新任务
    """
    return TaskService.create_task(db=db, task=task, creator_id=current_user_id)


@router.get("/", response_model=List[TaskResponse])
def read_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    获取任务列表，支持分页
    """
    return TaskService.get_tasks(db, skip=skip, limit=limit)


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
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    """
    更新任务信息
    """
    updated_task = TaskService.update_task(db, task_id=task_id, task=task)
    if updated_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
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
