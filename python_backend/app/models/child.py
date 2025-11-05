from sqlalchemy import Column, Integer, String, Date, Enum, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Child(Base):
    __tablename__ = "children"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    birthday = Column(Date, nullable=False)
    gender = Column(Enum('male', 'female'), nullable=False)  # Changed to match PHP's male/female
    avatar = Column(String(255), nullable=True)
    star_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    star_records = relationship("StarRecord", back_populates="child", cascade="all, delete-orphan")
    rewards = relationship("Reward", secondary="reward_children", back_populates="children")
