from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):
    model_config = {
        "env_file": str(BASE_DIR / ".env"),
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

    # DB
    database_user: str = Field(..., env="DATABASE_USER")
    database_pass: str = Field(..., env="DATABASE_PASS")
    database_host: str = Field("localhost", env="DATABASE_HOST")
    database_port: int = Field(5432, env="DATABASE_PORT")
    database_name: str = Field(..., env="DATABASE_NAME")
    database_url: Optional[str] = Field(None, env="DATABASE_URL")

    # Security
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field("HS256")
    access_token_expire_minutes: int = Field(60)

    env: str = Field("development")

    @property
    def sqlalchemy_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        return (
            f"postgresql+asyncpg://{self.database_user}:"
            f"{self.database_pass}@{self.database_host}:"
            f"{self.database_port}/{self.database_name}"
        )

@lru_cache()
def get_settings() -> Settings:
    return Settings()


