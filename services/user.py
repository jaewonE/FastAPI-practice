# services/user.py
import bcrypt
from typing import Optional
from schemas.user import User, CreateUserInput, UpdateUserInput, LoginUserInput
from error.exceptions import UserAlreadyExistsError, LoginFailedError, UserNotFoundError


class UserService:
    def __init__(self):
        self.users: dict[int, User] = {}
        self.counter = 0

    def create_user(self, payload: CreateUserInput) -> User:
        if len([u for u in self.users.values() if u.name == payload.name]) > 0:
            raise UserAlreadyExistsError(context={"name": payload.name})

        user_id = self.counter
        self.counter += 1
        payload.password = bcrypt.hashpw(
            payload.password.encode(), bcrypt.gensalt()).decode()
        user = User(id=user_id, todo_id_list=[], **payload.model_dump())
        self.users[user_id] = user
        return user

    def login_user(self, payload: LoginUserInput) -> User:
        for user in self.users.values():
            if user.name == payload.name and bcrypt.checkpw(payload.password.encode(), user.password.encode()):
                return user
        raise LoginFailedError(context={"name": payload.name})

    def get_user(self, user_id: int) -> User:
        user = self.users.get(user_id)
        if not user:
            raise UserNotFoundError(context={"user_id": user_id})
        return user

    def update_user(self, user_id: int, payload: UpdateUserInput) -> User:
        user = self.users.get(user_id)
        if not user:
            raise UserNotFoundError(context={"user_id": user_id})
        if payload.password:
            payload.password = bcrypt.hashpw(
                payload.password.encode(), bcrypt.gensalt()).decode()
        changes = payload.model_dump(exclude_unset=True)
        updated = user.model_copy(update=changes)  # 타입 검증 재수행
        self.users[user_id] = updated
        return updated

    def delete_user(self, user_id: int):
        if user_id in self.users:
            del self.users[user_id]
        else:
            raise UserNotFoundError(context={"user_id": user_id})


# 싱글톤 인스턴스 & DI 팩토리
user_service = UserService()


def get_user_service() -> UserService:
    return user_service
