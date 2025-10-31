from pydantic import BaseModel, Field
from typing import Optional

class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1)
    post_id: int
    author_id: Optional[int]

class CommentRead(BaseModel):
    id: int
    content: str
    post_id: int
    author_id: Optional[int]
    class Config:
        from_attributes = True
