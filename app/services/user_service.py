from repositories.user_repo import UserRepository
from schemas.user import UserCreate, UserRead
from models.user import User
from passlib.context import CryptContext
from core.security import get_password_hash, verify_password, create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
    
    async def create_user(self, payload: UserCreate):
        existing = await self.repo.get_by_email(payload.email)
        if existing:
            raise ValueError("Email already registered")
        hashed = get_password_hash(payload.password)
        user = User(email=payload.email, hashed_password=hashed)
        u = await self.repo.create(user)
        return UserRead.model_validate(u)

    async def authenticate_user(self, email: str, password: str):
        user = await self.repo.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    async def create_token_for_user(self, user) -> str:
        return create_access_token(subject=user.id)

    async def get_user(self, user_id: int):
        return await self.repo.get(user_id)
