from pydantic import BaseModel, EmailStr, Field, field_validator

class UserBase(BaseModel):
    email: EmailStr

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long.")

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        import re
        if not re.search(r"\d", v) or not re.search(r"[A-Z]", v):
            raise ValueError("The password must contain at least one digit and one uppercase letter.")
        return v

class UserRead(BaseModel):
    id: int
    email: EmailStr
    class Config:
        from_attributes = True
