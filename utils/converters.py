from schemas.user import User, UserOut


def remove_password(user: User) -> UserOut:
    data = user.model_dump()
    data.pop("password", None)
    return UserOut.model_validate(data)
