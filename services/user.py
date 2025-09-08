# services/user.py
import bcrypt
from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from schemas.user import User, CreateUserInput, UpdateUserInput, LoginUserInput
from error.exceptions import UserAlreadyExistsError, LoginFailedError, UserNotFoundError
from model import UserTable, TodoTable


def _todo_id_list(db: Session, user_id: int) -> list[int]:
    rows = db.execute(
        select(TodoTable.id).where(TodoTable.owner_id == user_id).order_by(TodoTable.id)
    ).scalars().all()
    return list(rows)


def _to_user_schema(row: UserTable, *, db: Session | None = None, with_todo_ids: bool = True) -> User:
    todo_ids: list[int] = []
    if with_todo_ids and db is not None:
        todo_ids = _todo_id_list(db, row.id)
    return User(id=row.id, name=row.name, password=row.password, todo_id_list=todo_ids)


class UserService:
    def __init__(self):
        pass

    def create_user(self, payload: CreateUserInput, *, db: Session) -> User:
        # 중복 체크
        exists = db.execute(select(UserTable.id).where(UserTable.name == payload.name)).first()
        if exists:
            raise UserAlreadyExistsError(context={"name": payload.name})

        hashed = bcrypt.hashpw(payload.password.encode(), bcrypt.gensalt()).decode()
        row = UserTable(name=payload.name, password=hashed)
        db.add(row)
        db.commit()
        db.refresh(row)
        return _to_user_schema(row, db=db)

    def login_user(self, payload: LoginUserInput, *, db: Session) -> User:
        row = db.execute(select(UserTable).where(UserTable.name == payload.name)).scalar_one_or_none()
        if not row or not bcrypt.checkpw(payload.password.encode(), row.password.encode()):
            raise LoginFailedError(context={"name": payload.name})
        return _to_user_schema(row, db=db)

    def get_user(self, user_id: int, *, db: Session) -> User:
        row = db.execute(select(UserTable).where(UserTable.id == user_id)).scalar_one_or_none()
        if not row:
            raise UserNotFoundError(context={"user_id": user_id})
        return _to_user_schema(row, db=db)

    def update_user(self, user_id: int, payload: UpdateUserInput, *, db: Session) -> User:
        row = db.execute(select(UserTable).where(UserTable.id == user_id)).scalar_one_or_none()
        if not row:
            raise UserNotFoundError(context={"user_id": user_id})

        changes = payload.model_dump(exclude_unset=True)
        if "password" in changes and changes["password"]:
            changes["password"] = bcrypt.hashpw(changes["password"].encode(), bcrypt.gensalt()).decode()
        for k, v in changes.items():
            setattr(row, k, v)
        db.add(row)
        db.commit()
        db.refresh(row)
        return _to_user_schema(row, db=db)

    def delete_user(self, user_id: int, *, db: Session) -> None:
        row = db.execute(select(UserTable).where(UserTable.id == user_id)).scalar_one_or_none()
        if not row:
            raise UserNotFoundError(context={"user_id": user_id})
        db.delete(row)
        db.commit()


# 싱글톤 인스턴스 & DI 팩토리
user_service = UserService()


def get_user_service() -> UserService:
    return user_service
