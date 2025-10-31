from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user import UserCreate, UserRead
from api.deps import get_user_repo
from repositories.user_repo import UserRepository
from services.user_service import UserService

router = APIRouter()

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, repo: UserRepository = Depends(get_user_repo)):
    svc = UserService(repo)
    try:
        return await svc.create_user(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, repo: UserRepository = Depends(get_user_repo)):
    user = await repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)

@router.get("/", response_model=list[UserRead])
async def list_users(limit: int = 50, offset: int = 0, repo: UserRepository = Depends(get_user_repo)):
    users = await repo.list(limit=limit, offset=offset)
    return [UserRead.model_validate(u) for u in users]
