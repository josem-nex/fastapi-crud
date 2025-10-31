from typing import AsyncGenerator
from fastapi import Depends
from db.session import get_session
from repositories.user_repo import UserRepository
from repositories.post_repo import PostRepository
from repositories.tag_repo import TagRepository
from repositories.comment_repo import CommentRepository
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncGenerator:
    async for session in get_session():
        yield session

def get_user_repo(session: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(session)

def get_post_repo(session: AsyncSession = Depends(get_db)) -> PostRepository:
    return PostRepository(session)

def get_tag_repo(session: AsyncSession = Depends(get_db)) -> TagRepository:
    return TagRepository(session)

def get_comment_repo(session: AsyncSession = Depends(get_db)) -> CommentRepository:
    return CommentRepository(session)
