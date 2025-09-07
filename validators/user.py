# validators/user.py
from typing import Annotated
from pydantic import BeforeValidator, StringConstraints
import re


def _name_trim_and_check(v):
    if isinstance(v, str):
        s = v.strip()
        if not s:
            raise ValueError("name must not be empty or whitespace")
        return s
    return v


UserName = Annotated[
    str,
    BeforeValidator(_name_trim_and_check),
    StringConstraints(min_length=1, max_length=100),
]


# 최소 8자, 최대 128자, 공백으로 시작/끝 금지, 문자/숫자 각각 1개 이상 포함
_PASSWORD_RE = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[ -~]+$")


def _password_validate(v):
    if not isinstance(v, str):
        return v
    if len(v) < 8 or len(v) > 128:
        raise ValueError("password must be between 8 and 128 characters")
    if v.strip() != v:
        raise ValueError(
            "password must not have leading or trailing whitespace")
    if not _PASSWORD_RE.match(v):
        raise ValueError(
            "password must contain at least one letter and one digit")
    return v


UserPassword = Annotated[
    str,
    BeforeValidator(_password_validate),
    StringConstraints(min_length=8, max_length=128),
]
