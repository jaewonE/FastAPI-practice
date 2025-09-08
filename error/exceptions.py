# error/exceptions.py
from typing import Any, Optional


class AppError(Exception):
    """도메인 계층의 기본 예외: 기본 메시지·코드·컨텍스트 보유"""
    default_message = "Application error"
    code = "APP_ERROR"

    def __init__(self, message: str | None = None, *, context: Optional[dict[str, Any]] = None):
        self.message = message or self.default_message
        self.context = context or {}
        super().__init__(self.message)


class UserAlreadyExistsError(AppError):
    """유저 중복(회원가입 시 중복된 사용자명 존재)"""
    default_message = "User already exists"
    code = "USER_ALREADY_EXISTS"


class LoginFailedError(AppError):
    """로그인 실패(계정 존재/비번 불일치 여부를 감춤)"""
    default_message = "Invalid username or password"
    code = "LOGIN_FAILED"


class UserNotFoundError(AppError):
    """유저 미존재(서비스 내부 검색 실패 등)"""
    default_message = "User not found"
    code = "USER_NOT_FOUND"


class TodoNotFoundError(AppError):
    """Todo 미존재(서비스 내부 검색 실패 등)"""
    default_message = "Todo not found"
    code = "TODO_NOT_FOUND"


class ImageNotFoundError(AppError):
    """이미지 미존재(서비스 내부 검색 실패 등)"""
    default_message = "Image not found"
    code = "IMAGE_NOT_FOUND"


class UnauthorizedError(AppError):
    """인가 실패(소유권 불일치 등)"""
    default_message = "Unauthorized"
    code = "UNAUTHORIZED"
