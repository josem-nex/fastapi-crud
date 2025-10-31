from fastapi import APIRouter, Depends, HTTPException, status, Query
from schemas.post import PostCreate, PostRead
from api.deps import get_post_repo, get_tag_repo, get_current_user
from repositories.post_repo import PostRepository
from repositories.tag_repo import TagRepository
from services.post_service import PostService
from pydantic import TypeAdapter

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(payload: PostCreate, current_user=Depends(get_current_user), post_repo: PostRepository = Depends(get_post_repo), tag_repo: TagRepository = Depends(get_tag_repo)):
    svc = PostService(post_repo, tag_repo)
    return await svc.create_post(payload, owner_id=current_user.id)

@router.get("/{post_id}", response_model=PostRead)
async def get_post(post_id: int, repo: PostRepository = Depends(get_post_repo)):
    post = await repo.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return PostRead.model_validate(post)

@router.get("/", response_model=list[PostRead])
async def list_posts(page: int = Query(1, ge=1), per_page: int = Query(10, ge=1, le=100), include_deleted: bool = Query(False), repo: PostRepository = Depends(get_post_repo)):
    offset = (page - 1) * per_page
    posts = await repo.list(limit=per_page, offset=offset, with_deleted=include_deleted)
    adapter = TypeAdapter(list[PostRead])
    return adapter.validate_python(posts)

@router.put("/{post_id}", response_model=PostRead)
async def update_post(post_id: int, payload: PostCreate, current_user=Depends(get_current_user), repo: PostRepository = Depends(get_post_repo)):
    post = await repo.get(post_id, with_deleted=False)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to update this post")
    post.title = payload.title
    post.content = payload.content
    await repo.update(post)
    return PostRead.model_validate(post)

# Delete (soft) post: solo owner
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, current_user=Depends(get_current_user), repo: PostRepository = Depends(get_post_repo)):
    post = await repo.get(post_id, with_deleted=False)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to delete this post")
    await repo.soft_delete(post)
    return None

@router.get("/deleted/", response_model=list[PostRead])
async def list_deleted(page: int = Query(1, ge=1), per_page: int = Query(10, ge=1, le=100), current_user=Depends(get_current_user), repo: PostRepository = Depends(get_post_repo)):
    offset = (page - 1) * per_page
    posts = await repo.list_deleted(limit=per_page, offset=offset)
    adapter = TypeAdapter(list[PostRead])
    return adapter.validate_python(posts)

@router.post("/{post_id}/restore", response_model=PostRead)
async def restore_post(post_id: int, current_user=Depends(get_current_user), repo: PostRepository = Depends(get_post_repo)):
    post = await repo.get(post_id, with_deleted=True)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to restore this post")
    restored = await repo.restore(post)
    return PostRead.from_orm(restored)
