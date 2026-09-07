from fastapi import HTTPException, status

from app.core.constants import ALLOW_USERNAME_SYMBOLS


def raise_http_422_exception(detail: str):
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        detail=detail
    )


def validate_attribute(attribute_name: str, content: str) -> None:
    string = content.lower()

    if string[0] == "_" or string[0] == "-":
        raise_http_422_exception(f"{attribute_name} cannot start with '_' or '-'")

    if string[-1] == "_" or string[-1] == "-":
        raise_http_422_exception(f"{attribute_name} cannot end with '_' or '-'")

    is_underscore_or_score: bool = False
    for char in string:
        if ALLOW_USERNAME_SYMBOLS.find(char) == -1:
            raise_http_422_exception(
                f"{attribute_name} can only contain: a-z (A-Z), 0-9, '_', '-'"
            )
        if (char == "-" or char == "_"):
            if is_underscore_or_score:
                raise_http_422_exception(
                    f"{attribute_name} cannot contain two or more '_'/'-' in a row"
                )
            is_underscore_or_score = True
        else:
            is_underscore_or_score = False
