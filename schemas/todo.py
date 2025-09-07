# schemas/todo.py
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from validators.string import TitleRule, OptionalDescriptionRule

"""
입력값을 검증하는 대표적인 방법 2가지
1. (CreateTodoInput 예제) 각각의 BaseModel 필드에 대해 Field()로 제약조건을 명시하고 field_validator()로 전처리/후처리 검증
2. (UpdateTodoInput 예제) 재사용 가능한 커스텀 타입을 정의하고, BaseModel 필드에 적용
"""


class Todo(BaseModel):
    id: int
    title: TitleRule
    description: OptionalDescriptionRule = None
    completed: bool = False


class CreateTodoInput(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    completed: bool = False

    @field_validator("title", mode="before")
    @classmethod
    def strip_title_if_present(cls, v):
        if v is None:
            return None
        s = v.strip()
        if not s:
            raise ValueError("title must not be empty or whitespace")
        return s

    @field_validator("description", mode="before")
    @classmethod
    def strip_description_if_present(cls, v):
        if v is None:
            return None
        s = v.strip()
        return s if s else None


class UpdateTodoInput(BaseModel):
    # 부분 업데이트: 보낸 필드만 반영
    title: Optional[TitleRule] = None
    description: OptionalDescriptionRule = None
    completed: Optional[bool] = None
