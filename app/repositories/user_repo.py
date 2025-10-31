from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from repositories.base import BaseRepository
from models.user import User

class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_email(self, email: str):
        q = select(User).where(User.email == email)
        q = q.where(User.is_deleted == False)
        r = await self.session.execute(q)
        return r.scalars().first()
