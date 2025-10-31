from repositories.user_repo import UserRepository
from schemas.user import UserCreate, UserRead
from models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create_user(self, payload: UserCreate) -> UserRead:
        existing = await self.repo.get_by_email(payload.email)
        if existing:
            raise ValueError("Email already registered")
        hashed = pwd_context.hash(payload.password)
        user = User(email=payload.email, hashed_password=hashed)
        u = await self.repo.create(user)
        return UserRead.model_validate(u)

    async def get_user(self, user_id: int):
        return await self.repo.get(user_id)
