from uuid import UUID, uuid4
from schemas.user import UserCreate, UserUpdate
from database import users


class UserService:

    def list_users(self):
        return users

    def get_user(self, user_id: UUID):
        return next((u for u in users if u["id"] == user_id), None)

    def create_user(self, user_in: UserCreate):
        new_user = {
            "id": uuid4(),
            "name": user_in.name,
            "email": user_in.email,
            "password": user_in.password  # Note: Plain-text for simplicity
        }
        users.append(new_user)
        return new_user

    def update_user(self, user_id: UUID, user_in: UserUpdate):
        user = self.get_user(user_id)
        if not user:
            return None
        if user_in.name:
            user["name"] = user_in.name
        if user_in.email:
            user["email"] = user_in.email
        return user

    def delete_user(self, user_id: UUID):
        user = self.get_user(user_id)
        if not user:
            return False
        users.remove(user)
        return True

    def login(self, email: str, password: str):
        return next((u for u in users if u["email"] == email and u["password"] == password), None)

    def change_password(self, user_id: UUID, old_password: str, new_password: str):
        user = self.get_user(user_id)
        if user and user["password"] == old_password:
            user["password"] = new_password
            return True
        return False


user_service = UserService()
