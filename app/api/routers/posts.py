from fastapi import APIRouter, Depends, HTTPException, status, Query
from schemas.post import PostCreate, PostRead
from api.deps import get_post_repo, get_tag_repo
from repositories.post_repo import PostRepository
from repositories.tag_repo import TagRepository
from services.post_service import PostService
from pydantic import TypeAdapter

router = APIRouter()

@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(payload: PostCreate, owner_id: int = Query(None), post_repo: PostRepository = Depends(get_post_repo), tag_repo: TagRepository = Depends(get_tag_repo)):
    svc = PostService(post_repo, tag_repo)
    if owner_id is None:
        raise HTTPException(status_code=400, detail="owner_id is required")
    return await svc.create_post(payload, owner_id)

@router.get("/{post_id}", response_model=PostRead)
async def get_post(post_id: int, repo: PostRepository = Depends(get_post_repo)):
    post = await repo.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return PostRead.model_validate(post)

@router.get("/", response_model=list[PostRead])
async def list_posts(limit: int = 50, offset: int = 0, repo: PostRepository = Depends(get_post_repo)):
    posts = await repo.list(limit=limit, offset=offset)
    adapter = TypeAdapter(list[PostRead])
    return adapter.validate_python(posts)

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, repo: PostRepository = Depends(get_post_repo)):
    post = await repo.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    await repo.soft_delete(post)
    return None
