from pydantic import BaseModel, Field
from typing import List, Optional
from schemas.tag import TagRead

class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: Optional[str] = Field(None)

class PostCreate(PostBase):
    tags: Optional[List[str]] = Field(default_factory=list)

class PostRead(PostBase):
    id: int
    owner_id: Optional[int]
    tags: List[TagRead] = Field(default_factory=list)
    class Config:
        from_attributes = True
        
