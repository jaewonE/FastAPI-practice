# apis/user.py
from fastapi import APIRouter, Response, status, HTTPException, Depends, Request
from schemas.user import UserOut, CreateUserInput, UpdateUserInput, LoginUserInput, UserWithTokenOutput
from services.user import UserService, get_user_service
from utils.converters import remove_password
from auth.auth_bearer import JWTBearer
from auth.auth_handler import signJWT
from sqlalchemy.orm import Session
from db import get_db_session

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


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
    db: Session = Depends(get_db_session),
) -> UserOut:
    user = svc.create_user(payload, db=db)
    return remove_password(user)


@router.get(
    "/me",
    response_model=UserWithTokenOutput,
    response_model_exclude_none=True,
    summary="Get the current user",
    dependencies=[Depends(JWTBearer())]
)
def get_user(
    user_id: str = Depends(JWTBearer()),
    svc: UserService = Depends(get_user_service),
    db: Session = Depends(get_db_session),
) -> UserWithTokenOutput:
    user = svc.get_user(int(user_id), db=db)
    access_token = signJWT(user.id)
    return UserWithTokenOutput(user=remove_password(user), access_token=access_token)


@router.post(
    "/login",
    response_model=UserWithTokenOutput,
    response_model_exclude_none=True,
    summary="Login a user",
)
def login_user(
    payload: LoginUserInput,
    svc: UserService = Depends(get_user_service),
    db: Session = Depends(get_db_session),
) -> UserWithTokenOutput:
    user = svc.login_user(payload, db=db)
    access_token = signJWT(user.id)
    return UserWithTokenOutput(user=remove_password(user), access_token=access_token)


@router.patch(
    "",
    response_model=UserOut,
    response_model_exclude_none=True,
    summary="Partially update a user by ID",
    dependencies=[Depends(JWTBearer())]
)
def update_user(
    payload: UpdateUserInput,
    response: Response,
    user_id: str = Depends(JWTBearer()),
    svc: UserService = Depends(get_user_service),
    db: Session = Depends(get_db_session),
) -> UserOut:
    user = svc.update_user(int(user_id), payload, db=db)
    response.headers["ETag"] = f'W/"user-{user.id}-0"'
    return remove_password(user)


@router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete the current user",
    dependencies=[Depends(JWTBearer())]
)
def delete_user(
    user_id: str = Depends(JWTBearer()),
    svc: UserService = Depends(get_user_service),
    db: Session = Depends(get_db_session),
) -> None:
    svc.delete_user(int(user_id), db=db)
    return None
