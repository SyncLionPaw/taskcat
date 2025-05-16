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
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # New fields to be added in migration
    difficulty = Column(Integer, default=1, nullable=True)  # 1-5 scale for task difficulty
    points = Column(Integer, default=0, nullable=True)  # Points/score value for the task

    publish_type = Column(Integer,  default=1, nullable=False)
    deadline = Column(DateTime, nullable=True)

    material_id = Column(Integer, ForeignKey("materials.id"), nullable=True)  # 改为允许为空

    # 关系定义
    creator = relationship(
        "User", foreign_keys=[creator_id], back_populates="created_tasks"
    )
    assignee = relationship(
        "User", foreign_keys=[assignee_id], back_populates="assigned_tasks"
    )
    material = relationship("Material", back_populates="tasks")  # 添加与Material的关系

    def __repr__(self):
        return f"<Task(id={self.id}, title={self.title})>"
