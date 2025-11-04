from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

# Association table for many-to-many relationship
child_reward = Table(
    'child_reward',
    Base.metadata,
    Column('child_id', Integer, ForeignKey('children.id'), primary_key=True),
    Column('reward_id', Integer, ForeignKey('rewards.id'), primary_key=True),
    Column('created_at', DateTime, server_default=func.now())
)

class Reward(Base):
    __tablename__ = "rewards"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    star_cost = Column(Integer, nullable=False)
    image = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    children = relationship("Child", secondary=child_reward, back_populates="rewards")
