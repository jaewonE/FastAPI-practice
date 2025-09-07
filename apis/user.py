# apis/user.py
from fastapi import APIRouter, Response, status, HTTPException, Depends, Request
from schemas.user import UserOut, CreateUserInput, UpdateUserInput, LoginUserInput
from services.user import UserService, get_user_service
from utils.converters import remove_password

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


def _set_creation_headers(request: Request, response: Response, user_id: int):
    location_url = request.url_for("get_user", user_id=user_id)
    response.headers["Location"] = str(location_url)
    response.headers["ETag"] = f'W/"user-{user_id}-0"'


@router.post(
    "",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
    summary="Create a new user",
)
def create_user(
    payload: CreateUserInput,
    response: Response,
    request: Request,
    svc: UserService = Depends(get_user_service),
) -> UserOut:
    user = svc.create_user(payload)
    _set_creation_headers(request, response, user.id)
    return remove_password(user)


@router.get(
    "/{user_id}",
    response_model=UserOut,
    response_model_exclude_none=True,
    summary="Get a user by ID",
)
def get_user(
    user_id: int,
    svc: UserService = Depends(get_user_service),
) -> UserOut:
    user = svc.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return remove_password(user)


@router.post(
    "/login",
    response_model=UserOut,
    response_model_exclude_none=True,
    summary="Login a user",
)
def login_user(
    payload: LoginUserInput,
    svc: UserService = Depends(get_user_service),
) -> UserOut:
    user = svc.login_user(payload)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return remove_password(user)


@router.patch(
    "/{user_id}",
    response_model=UserOut,
    response_model_exclude_none=True,
    summary="Partially update a user by ID",
)
def update_user(
    user_id: int,
    payload: UpdateUserInput,
    response: Response,
    svc: UserService = Depends(get_user_service),
) -> UserOut:
    user = svc.update_user(user_id, payload)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    response.headers["ETag"] = f'W/"user-{user.id}-0"'
    return remove_password(user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user by ID",
)
def delete_user(
    user_id: int,
    svc: UserService = Depends(get_user_service),
) -> None:
    ok = svc.delete_user(user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return None
