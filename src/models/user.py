from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    
    # Make nullable to handle existing records without these columns
    is_active = Column(Boolean, default=True, nullable=True)
    is_superuser = Column(Boolean, default=False, nullable=True)
    
    # Add server_default for existing records
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=True)

    # Define relationships
    tasks_created = relationship("Task", back_populates="creator", foreign_keys="[Task.creator_id]", lazy="dynamic")