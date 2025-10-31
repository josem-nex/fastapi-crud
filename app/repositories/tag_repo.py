from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from repositories.base import BaseRepository
from models.tag import Tag

class TagRepository(BaseRepository[Tag]):
    def __init__(self, session: AsyncSession):
        super().__init__(Tag, session)

    async def get_by_name(self, name: str):
        q = select(Tag).where(Tag.name == name).where(Tag.is_deleted == False)
        r = await self.session.execute(q)
        return r.scalars().first()
