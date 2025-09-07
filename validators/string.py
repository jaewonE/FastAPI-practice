# validators/string.py
from typing import Optional, Annotated
from pydantic import BeforeValidator, StringConstraints


def _trim(v):
    return v.strip() if isinstance(v, str) else v


def _none_if_empty(v):
    if isinstance(v, str):
        s = v.strip()
        return s if s else None
    return v


# 제목 규칙: 공백 제거 → 최소 길이 보장(=빈 문자열 금지), 최대 길이 제한
TitleRule = Annotated[
    str,
    BeforeValidator(_trim),
    StringConstraints(min_length=1, max_length=200),
]

# 일반 문자열 규칙: 공백 제거 → 최소 길이 보장(=빈 문자열 금지), 최대 길이 제한
DescriptionRule = Annotated[
    str,
    BeforeValidator(_trim),
    StringConstraints(min_length=1, max_length=2000),
]

# 공백 제거 → 비면 None, 최대 길이 제한(문자열일 때만 적용)
OptionalDescriptionRule = Annotated[
    Optional[str],
    BeforeValidator(_none_if_empty),
    StringConstraints(max_length=2000),
]
