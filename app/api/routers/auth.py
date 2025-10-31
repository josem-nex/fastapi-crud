from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from api.deps import get_user_repo
from repositories.user_repo import UserRepository
from schemas.user import UserCreate, UserRead
from schemas.token import Token
from services.user_service import UserService

router = APIRouter()

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, repo: UserRepository = Depends(get_user_repo)):
    svc = UserService(repo)
    try:
        return await svc.create_user(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), repo: UserRepository = Depends(get_user_repo)):
    svc = UserService(repo)
    user = await svc.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")
    
    access_token = await svc.create_token_for_user(user)
    return {"access_token": access_token, "token_type": "bearer"}
