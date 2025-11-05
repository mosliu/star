from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey, DateTime, func, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

# Association table for many-to-many relationship with deduction amount
# This matches PHP's reward_children table structure
reward_children = Table(
    'reward_children',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('reward_id', Integer, ForeignKey('rewards.id'), nullable=False),
    Column('child_id', Integer, ForeignKey('children.id'), nullable=False),
    Column('deduction_amount', Integer, nullable=True),  # Actual stars deducted when redeemed
    Column('created_at', DateTime, server_default=func.now()),
    Column('updated_at', DateTime, server_default=func.now(), onupdate=func.now())
)

class Reward(Base):
    __tablename__ = "rewards"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    star_cost = Column(Integer, nullable=False)
    image = Column(String(255), nullable=True)
    is_redeemed = Column(Boolean, default=False, nullable=False)
    redeemed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    children = relationship("Child", secondary=reward_children, back_populates="rewards")
