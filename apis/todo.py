# apis/todo.py
from fastapi import APIRouter, Response, status, HTTPException, Depends, Request
from schemas.todo import Todo, CreateTodoInput, UpdateTodoInput
from services.todo import TodoService, get_todo_service

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}},
)


def _set_creation_headers(request: Request, response: Response, todo_out: Todo):
    # RFC 관례: Location + (선택) Weak ETag + Last-Modified
    location_url = request.url_for("get_todo", todo_id=todo_out.id)
    response.headers["Location"] = str(location_url)
    updated_ts = 0
    response.headers["ETag"] = f'W/"todo-{todo_out.id}-{updated_ts}"'


@router.post(
    "",  # POST /todos
    response_model=Todo,
    status_code=status.HTTP_201_CREATED,  # 성공시 201, 지정하지 않을 경우 자동 200.
    response_model_exclude_none=True,
    summary="Create a new todo"
)
def create_todo(
    payload: CreateTodoInput,
    response: Response,  # 타입 기반 변수 주입. 다른 명칭 가능
    request: Request,
    svc: TodoService = Depends(get_todo_service),
) -> Todo:
    todo_out = svc.create_todo(payload)
    _set_creation_headers(request, response, todo_out)
    return todo_out


@router.get(
    "/all",  # GET /todos/all
    response_model=list[Todo],
    response_model_exclude_none=True,
    summary="Get all todos",
)
def get_all_todos(
    svc: TodoService = Depends(get_todo_service),
) -> list[Todo]:
    return svc.get_all_todos()


@router.get(
    "/{todo_id}",  # GET /todos/{todo_id}
    response_model=Todo,
    response_model_exclude_none=True,
    summary="Get a todo by ID"
)
def get_todo(
    todo_id: int,
    svc: TodoService = Depends(get_todo_service),
) -> Todo:
    todo = svc.get_todo(todo_id)
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
) -> Todo:
    todo = svc.update_todo(todo_id, payload)
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
) -> None:
    svc.delete_todo(todo_id)
    return None
