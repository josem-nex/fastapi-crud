from fastapi import APIRouter, Depends, HTTPException, status
from schemas.tag import TagCreate, TagRead
from api.deps import get_tag_repo
from repositories.tag_repo import TagRepository
from models.tag import Tag
from services.tag_service import TagService

router = APIRouter()

@router.post("/", response_model=TagRead, status_code=status.HTTP_201_CREATED)
async def create_tag(payload: TagCreate, repo: TagRepository = Depends(get_tag_repo)):
    svc = TagService(repo)
    try:
        return await svc.create_tag(payload.name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[TagRead])
async def list_tags(limit: int = 50, offset: int = 0, repo: TagRepository = Depends(get_tag_repo)):
    tags = await repo.list(limit=limit, offset=offset)
    return [TagRead.model_validate(t) for t in tags]
