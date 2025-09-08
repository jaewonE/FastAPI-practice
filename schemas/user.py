# schemas/user.py
from typing import Optional, List
from pydantic import BaseModel, Field
from validators.user import UserName, UserPassword


class User(BaseModel):
    id: int
    name: UserName
    password: UserPassword
    todo_id_list: List[int] = Field(default_factory=list)


class UserOut(BaseModel):
    id: int
    name: UserName
    todo_id_list: List[int] = Field(default_factory=list)


class UserWithTokenOutput(BaseModel):
    user: UserOut
    access_token: str


class CreateUserInput(BaseModel):
    name: UserName
    password: UserPassword


class LoginUserInput(BaseModel):
    name: UserName
    password: UserPassword


class UpdateUserInput(BaseModel):
    name: Optional[UserName] = None
    password: Optional[UserPassword] = None
