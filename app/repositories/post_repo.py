from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from repositories.base import BaseRepository
from models.post import Post
from typing import Optional, TypeVar, List, Tuple

ModelType = TypeVar("ModelType")

class PostRepository(BaseRepository[Post]):
    def __init__(self, session: AsyncSession):
        super().__init__(Post, session)

    async def list_by_owner(self, owner_id: int, limit: int = 50, offset: int = 0):
        q = select(Post).where(Post.owner_id == owner_id).where(Post.is_deleted == False).limit(limit).offset(offset)
        r = await self.session.execute(q)
        return r.scalars().all()
    
    async def list(self, limit: int = 50, offset: int = 0, with_deleted = False) -> List[Post]:
        if with_deleted:
            stmt = (
                select(Post)
                .options(selectinload(Post.tags)) 
                .limit(limit)
                .offset(offset)
            )
        else:
            stmt = (
                select(Post)
                .options(selectinload(Post.tags)) 
                .limit(limit)
                .offset(offset)
                .where(Post.is_deleted == False)
            )
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def list_deleted(self, *, limit: int = 50, offset: int = 0) -> List[ModelType]:
        if not hasattr(self.model, "is_deleted"):
            return []
        q = select(self.model).where(self.model.is_deleted == True).limit(limit).offset(offset).options(selectinload(Post.tags))
        r = await self.session.execute(q)
        return r.scalars().all()    


    async def get(self, id: int, with_deleted: bool = False) -> Optional[ModelType]:
        q = select(self.model).where(self.model.id == id).options(selectinload(Post.tags))
        if hasattr(self.model, "is_deleted") and not with_deleted:
            q = q.where(self.model.is_deleted == False)
        result = await self.session.execute(q)
        return result.scalars().first()