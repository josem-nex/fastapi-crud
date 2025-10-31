from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from repositories.base import BaseRepository
from models.comments import Comment

class CommentRepository(BaseRepository[Comment]):
    def __init__(self, session: AsyncSession):
        super().__init__(Comment, session)

    async def list_for_post(self, post_id: int, limit: int = 50, offset: int = 0):
        q = select(Comment).where(Comment.post_id == post_id).where(Comment.is_deleted == False).limit(limit).offset(offset)
        r = await self.session.execute(q)
        return r.scalars().all()
