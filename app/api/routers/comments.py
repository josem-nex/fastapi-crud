from fastapi import APIRouter, Depends, HTTPException, status
from api.deps import get_comment_repo, get_post_repo, get_user_repo
from repositories.comment_repo import CommentRepository
from repositories.post_repo import PostRepository
from repositories.user_repo import UserRepository
from schemas.comment import CommentCreate, CommentRead
from models.comments import Comment

router = APIRouter()

@router.post("/", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
async def create_comment(payload: CommentCreate, comment_repo: CommentRepository = Depends(get_comment_repo), post_repo: PostRepository = Depends(get_post_repo), user_repo: UserRepository = Depends(get_user_repo)):
    post = await post_repo.get(payload.post_id)
    # post exists
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if payload.author_id:
    # author exists
        author = await user_repo.get(payload.author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
    comment = Comment(content=payload.content, post_id=payload.post_id, author_id=payload.author_id)
    c = await comment_repo.create(comment)
    return CommentRead.model_validate(c)
