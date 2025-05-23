from pydantic import BaseModel, EmailStr
from uuid import UUID, uuid4

class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: UUID


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PasswordChange(BaseModel):
    old_password: str
    new_password: str
