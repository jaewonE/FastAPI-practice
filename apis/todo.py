# apis/todo.py
from fastapi import APIRouter, Response, status, Depends, Request
from db import get_db_session
from schemas.todo import Todo, CreateTodoInput, UpdateTodoInput
from services.todo import TodoService, get_todo_service
from auth.auth_bearer import JWTBearer
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(JWTBearer())]
)


@router.post(
    "",  # POST /todos
    response_model=Todo,
    status_code=status.HTTP_201_CREATED,  # 성공시 201, 지정하지 않을 경우 자동 200.
    response_model_exclude_none=True,
    summary="Create a new todo",
)
def create_todo(
    payload: CreateTodoInput,
    svc: TodoService = Depends(get_todo_service),
    user_id: str = Depends(JWTBearer()),
    db: Session = Depends(get_db_session),
) -> Todo:
    todo_out = svc.create_todo(
        payload, user_id=int(user_id), db=db
    )
    return todo_out


@router.get(
    "/all",  # GET /todos/all
    response_model=list[Todo],
    response_model_exclude_none=True,
    summary="Get all todos",
)
def get_all_todos(
    svc: TodoService = Depends(get_todo_service),
    user_id: str = Depends(JWTBearer()),
    db: Session = Depends(get_db_session),
) -> list[Todo]:
    return svc.get_all_todos(user_id=int(user_id), db=db)


@router.get(
    "/{todo_id}",  # GET /todos/{todo_id}
    response_model=Todo,
    response_model_exclude_none=True,
    summary="Get a todo by ID"
)
def get_todo(
    todo_id: int,
    svc: TodoService = Depends(get_todo_service),
    user_id: str = Depends(JWTBearer()),
    db: Session = Depends(get_db_session),
) -> Todo:
    todo = svc.get_todo(todo_id, user_id=int(user_id), db=db)
    return todo


@router.patch(
    "/{todo_id}",  # PATCH /todos/{todo_id}
    response_model=Todo,
    response_model_exclude_none=True,
    summary="Partially update a todo by ID",
)
def update_todo(
    todo_id: int,
    payload: UpdateTodoInput,
    response: Response,
    svc: TodoService = Depends(get_todo_service),
    user_id: str = Depends(JWTBearer()),
    db: Session = Depends(get_db_session),
) -> Todo:
    todo = svc.update_todo(todo_id, payload, user_id=int(user_id), db=db)
    # 간단한 Weak ETag 재설정
    response.headers["ETag"] = f'W/"todo-{todo.id}-0"'
    return todo


@router.delete(
    "/{todo_id}",  # DELETE /todos/{todo_id}
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a todo by ID",
)
def delete_todo(
    todo_id: int,
    svc: TodoService = Depends(get_todo_service),
    user_id: str = Depends(JWTBearer()),
    db: Session = Depends(get_db_session),
) -> None:
    svc.delete_todo(todo_id, user_id=int(user_id), db=db)
    return None
