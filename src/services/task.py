from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate

class TaskService:
    @staticmethod
    def get_tasks(db: Session, skip: int = 0, limit: int = 100) -> List[Task]:
        return db.query(Task).offset(skip).limit(limit).all()

    @staticmethod
    def get_task(db: Session, task_id: int) -> Optional[Task]:
        return db.query(Task).filter(Task.id == task_id).first()

    @staticmethod
    def create_task(db: Session, task: TaskCreate, creator_id: int) -> Task:
        db_task = Task(
            **task.model_dump(),
            creator_id=creator_id
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def update_task(db: Session, task_id: int, task: TaskUpdate) -> Optional[Task]:
        db_task = TaskService.get_task(db, task_id)
        if not db_task:
            return None

        update_data = task.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)
            
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def delete_task(db: Session, task_id: int) -> bool:
        db_task = TaskService.get_task(db, task_id)
        if not db_task:
            return False
        
        db.delete(db_task)
        db.commit()
        return True