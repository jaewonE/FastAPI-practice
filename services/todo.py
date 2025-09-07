# services/todo.py
from typing import Optional
from schemas.todo import Todo, CreateTodoInput, UpdateTodoInput


class TodoService:
    def __init__(self):
        self.todos: dict[int, Todo] = {}  # 임시 DB. id를 key로 사용.
        self.counter = 0

    def create_todo(self, payload: CreateTodoInput) -> Todo:
        todo_id = self.counter
        self.counter += 1
        todo = Todo(
            id=todo_id,
            title=payload.title.strip(),
            description=(payload.description.strip()
                         if payload.description else None),
            completed=payload.completed,
        )
        self.todos[todo_id] = todo
        return todo

    def get_todo(self, todo_id: int) -> Optional[Todo]:
        return self.todos.get(todo_id)

    def get_all_todos(self) -> list[Todo]:
        return sorted(self.todos.values(), key=lambda t: t.id)

    def update_todo(self, todo_id: int, payload: UpdateTodoInput) -> Optional[Todo]:
        todo = self.todos.get(todo_id)
        if not todo:
            return None

        changes = payload.model_dump(exclude_unset=True)

        # 복사하여 스키마를 재정의하는 과정에서 타입 검증을 다시 수행함.
        updated = todo.model_copy(update=changes)
        self.todos[todo_id] = updated
        return updated

    def delete_todo(self, todo_id: int) -> bool:
        if todo_id in self.todos:
            del self.todos[todo_id]
            return True
        return False


# 싱글톤 서비스 인스턴스 (추후 DI 컨테이너/Repo 교체 지점)
todo_service = TodoService()


# 의존성 주입용 Wrapper
def get_todo_service() -> TodoService:
    """FastAPI Depends 주입용 팩토리"""
    return todo_service
