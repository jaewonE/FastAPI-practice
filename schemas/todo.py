# schemas/todo.py
from typing import Optional
from pydantic import BaseModel


class Todo(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool = False


class CreateTodoInput(BaseModel):
    title: str
    description: Optional[str]
    completed: bool


class UpdateTodoInput(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
