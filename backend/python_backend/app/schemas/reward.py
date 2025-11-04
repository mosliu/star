from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class RewardBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    star_cost: int = Field(..., ge=1, le=1000)
    
class RewardCreate(RewardBase):
    pass
    
class RewardUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    star_cost: Optional[int] = Field(None, ge=1, le=1000)
    image: Optional[str] = None
    
class RewardResponse(RewardBase):
    id: int
    image: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        
class RedeemRequest(BaseModel):
    child_id: int = Field(..., ge=1)
