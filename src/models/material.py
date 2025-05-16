from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.core.database import Base

class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    file_url = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)
    
    # 外键关联
    uploader_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 时间戳
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # 定义与User的关系
    uploader = relationship("User", back_populates="materials")
    # 添加与Task的关系
    tasks = relationship("Task", back_populates="material", lazy="dynamic")
    
    def __repr__(self):
        return f"<Material(id={self.id}, title={self.title})>"
