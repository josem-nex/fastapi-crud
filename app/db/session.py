from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.config import settings

DATABASE_URL = settings.database_url 

engine = create_async_engine(DATABASE_URL, future=True, echo=False)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

# Dependency
async def get_session():
    async with async_session() as session:
        yield session
