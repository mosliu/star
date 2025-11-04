from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal

class StarAdd(BaseModel):
    amount: int = Field(..., ge=1, le=100)
    reason: Optional[str] = Field(None, max_length=255)
    
class StarSubtract(BaseModel):
    amount: int = Field(..., ge=1, le=100)
    reason: Optional[str] = Field(None, max_length=255)
    
class StarRecordResponse(BaseModel):
    id: int
    child_id: int
    type: Literal["add", "subtract", "redeem"]
    amount: int
    reason: Optional[str]
    reward_id: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True
