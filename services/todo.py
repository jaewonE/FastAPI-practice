# services/todo.py
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from schemas.todo import Todo, CreateTodoInput, UpdateTodoInput
from error.exceptions import TodoNotFoundError, UserNotFoundError
from model import TodoTable, UserTable


def _to_todo_schema(row: TodoTable) -> Todo:
    return Todo.model_validate(row)


class TodoService:
    def __init__(self):
        pass

    def create_todo(self, payload: CreateTodoInput, *, user_id: int, db: Session) -> Todo:
        # 사용자 존재 검증 FK 오류 방지를 위한 사전 검증
        user = db.execute(select(UserTable).where(
            UserTable.id == user_id)).scalar_one_or_none()
        if not user:
            raise UserNotFoundError(context={"user_id": user_id})

        row = TodoTable(
            title=payload.title,
            description=payload.description,
            completed=payload.completed,
            owner_id=user_id,
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return _to_todo_schema(row)

    def get_todo(self, todo_id: int, *, user_id: int, db: Session) -> Todo:
        row = db.execute(
            select(TodoTable).where(TodoTable.id ==
                                    todo_id, TodoTable.owner_id == user_id)
        ).scalar_one_or_none()
        if not row:
            raise TodoNotFoundError(context={"todo_id": todo_id})
        return _to_todo_schema(row)

    def get_all_todos(self, *, user_id: int, db: Session) -> list[Todo]:
        rows = db.execute(
            select(TodoTable).where(TodoTable.owner_id ==
                                    user_id).order_by(TodoTable.id)
        ).scalars().all()
        return [
            _to_todo_schema(row) for row in rows
        ]

    def update_todo(self, todo_id: int, payload: UpdateTodoInput, *, user_id: int, db: Session) -> Todo:
        row = db.execute(
            select(TodoTable).where(TodoTable.id ==
                                    todo_id, TodoTable.owner_id == user_id)
        ).scalar_one_or_none()
        if not row:
            raise TodoNotFoundError(context={"todo_id": todo_id})

        changes = payload.model_dump(exclude_unset=True)
        for k, v in changes.items():
            setattr(row, k, v)
        db.add(row)
        db.commit()
        db.refresh(row)
        return _to_todo_schema(row)

    def delete_todo(self, todo_id: int, *, user_id: int, db: Session) -> None:
        row = db.execute(
            select(TodoTable).where(TodoTable.id ==
                                    todo_id, TodoTable.owner_id == user_id)
        ).scalar_one_or_none()
        if not row:
            raise TodoNotFoundError(context={"todo_id": todo_id})
        db.delete(row)
        db.commit()


# 싱글톤 서비스 인스턴스 (추후 DI 컨테이너/Repo 교체 지점)
todo_service = TodoService()


# 의존성 주입용 Wrapper
def get_todo_service() -> TodoService:
    """FastAPI Depends 주입용 팩토리"""
    return todo_service
