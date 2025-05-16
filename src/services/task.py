from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate

class TaskService:
    @staticmethod
    def get_tasks(db: Session, params: Dict[str, Any] = None) -> List[Task]:
        """
        Get all tasks with optional filtering
        """
        query = db.query(Task)
        
        # Apply filters if params are provided
        if params:
            if "status" in params:
                query = query.filter(Task.status == params["status"])
            if "assignee_id" in params:
                query = query.filter(Task.assignee_id == params["assignee_id"])
            if "creator_id" in params:
                query = query.filter(Task.creator_id == params["creator_id"])
        
        # Make sure to return all columns from the Task model
        return query.all()

    @staticmethod
    def get_task(db: Session, task_id: int) -> Optional[Task]:
        return db.query(Task).filter(Task.id == task_id).first()

    @staticmethod
    def create_task(db: Session, task: TaskCreate, creator_id: int) -> Task:
        db_task = Task(
            title=task.title,
            description=task.description,
            status=task.status or "pending",
            progress=task.progress or 0,
            creator_id=creator_id,
            difficulty=task.difficulty,  # Include difficulty
            points=task.points  # Include points
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