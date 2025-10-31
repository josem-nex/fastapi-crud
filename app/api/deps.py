from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_session
from repositories.user_repo import UserRepository
from repositories.post_repo import PostRepository
from repositories.tag_repo import TagRepository
from repositories.comment_repo import CommentRepository
from core.security import oauth2_scheme, decode_access_token
from models.user import User

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

async def get_current_user(token: str = Depends(oauth2_scheme), repo: UserRepository = Depends(get_user_repo)) -> User:
    payload = decode_access_token(token)
    sub = payload.get("sub")
    if sub is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    user = None
    try:
        user_id = int(sub)
        user = await repo.get(user_id)
    except Exception:
        user = await repo.get_by_email(sub)

    if not user or getattr(user, "is_deleted", False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado o inactivo")
    return user

