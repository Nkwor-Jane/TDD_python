from fastapi import APIRouter, HTTPException
from uuid import UUID

from schemas.user import UserCreate, UserResponse, UserUpdate, UserLogin, PasswordChange
from services.user import user_service

user_router = APIRouter()


@user_router.get("", response_model=list[UserResponse])
def list_users():
    return user_service.list_users()


@user_router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: UUID):
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.post("", response_model=UserResponse)
def create_user(user: UserCreate):
    new_user = user_service.create_user(user)
    return new_user


@user_router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: UUID, user: UserUpdate):
    updated = user_service.update_user(user_id, user)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@user_router.delete("/{user_id}")
def delete_user(user_id: UUID):
    success = user_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


@user_router.post("/login")
def login(credentials: UserLogin):
    user = user_service.login(credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "user_id": user["id"]}


@user_router.post("/{user_id}/change-password")
def change_password(user_id: UUID, passwords: PasswordChange):
    success = user_service.change_password(user_id, passwords.old_password, passwords.new_password)
    if not success:
        raise HTTPException(status_code=400, detail="Old password is incorrect or user not found")
    return {"message": "Password updated successfully"}
