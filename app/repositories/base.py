import datetime
from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, id: int, with_deleted: bool = False) -> Optional[ModelType]:
        q = select(self.model).where(self.model.id == id)
        if hasattr(self.model, "is_deleted") and not with_deleted:
            q = q.where(self.model.is_deleted == False)
        result = await self.session.execute(q)
        return result.scalars().first()

    async def list(self, *, limit: int = 50, offset: int = 0, with_deleted: bool = False) -> List[ModelType]:
        q = select(self.model).limit(limit).offset(offset)
        if hasattr(self.model, "is_deleted") and not with_deleted:
            q = q.where(self.model.is_deleted == False)
        result = await self.session.execute(q)
        return result.scalars().all()

    async def create(self, obj: ModelType) -> ModelType:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, obj: ModelType) -> ModelType:
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def soft_delete(self, obj: ModelType) -> ModelType:
        if hasattr(obj, "is_deleted"):
            obj.is_deleted = True
            if hasattr(obj, "deleted_at"):
                obj.deleted_at = datetime.datetime.now(datetime.timezone.utc)
            await self.session.commit()
            return obj

        await self.session.delete(obj)
        await self.session.commit()
        return obj
