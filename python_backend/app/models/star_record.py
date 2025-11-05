from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base

class StarRecord(Base):
    __tablename__ = "star_records"
    
    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    type = Column(Enum('add', 'subtract', 'redeem'), nullable=False)
    amount = Column(Integer, nullable=False)
    reason = Column(String(255), nullable=True)
    reward_id = Column(Integer, ForeignKey("rewards.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    child = relationship("Child", back_populates="star_records")
    reward = relationship("Reward")
