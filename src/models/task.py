from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.core.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text(length=16777215), nullable=True)  # mediumtext
    status = Column(String(20), nullable=True)
    progress = Column(Float, nullable=True)

    # Foreign keys
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)

    # New fields to be added in migration
    difficulty = Column(Integer, default=1, nullable=True)  # 1-5 scale for task difficulty
    points = Column(Integer, default=0, nullable=True)  # Points/score value for the task

    # Make sure these relationship definitions match the ones in User model
    creator = relationship(
        "User", foreign_keys=[creator_id], back_populates="created_tasks"
    )
    assignee = relationship(
        "User", foreign_keys=[assignee_id], back_populates="assigned_tasks"
    )
