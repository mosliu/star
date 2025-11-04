from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List, Literal
from .star import StarRecordResponse

class ChildBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    birthday: date
    gender: Literal["boy", "girl"]
    
class ChildCreate(ChildBase):
    pass
    
class ChildUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    birthday: Optional[date] = None
    gender: Optional[Literal["boy", "girl"]] = None
    avatar: Optional[str] = None
    
class ChildResponse(ChildBase):
    id: int
    age: int
    avatar: Optional[str]
    star_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True
        
class ChildDetailResponse(ChildResponse):
    star_records: List[StarRecordResponse] = []
    
    class Config:
        from_attributes = True
