from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from src.core.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    
    # Foreign keys
    creator_id = Column(Integer, ForeignKey("users.id"))
    
    # Add any other fields you need
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Define the relationship with User
    creator = relationship("User", back_populates="tasks_created", foreign_keys=[creator_id])
    
    # Add any other relationships