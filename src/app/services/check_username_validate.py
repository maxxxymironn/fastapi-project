from fastapi import HTTPException, status

from app.core.constants import ALLOW_USERNAME_SYMBOLS


def check_username(username: str) -> None:
    string = username.lower()

    if string[0] == "_" or string[0] == "-":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="username cannot start with '_' or '-'",
        )

    if string[-1] == "_" or string[-1] == "-":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="username cannot end with '_' or '-'",
        )

    is_underscore_or_score: bool = False
    for char in string:
        if ALLOW_USERNAME_SYMBOLS.find(char) == -1:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="username can only contain: a-z, 0-9, '_', '-'",
            )
        if (char == "-" or char == "_"):
            if is_underscore_or_score:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail="username cannot contain two or more '_'/'-' in a row",
                )
            is_underscore_or_score = True
        else:
            is_underscore_or_score = False
