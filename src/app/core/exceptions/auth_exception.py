from fastapi import HTTPException, status

from app.core.exceptions.base_domain_exception import BaseDomainException


class CredentialsException(HTTPException):
    def __init__(self, detail: str) -> None:
        self.detail = detail

        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )


class AlreadyAuthenticatedException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already authenticated"
        )


class NotAdminException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not an admin",
        )


class WrongPasswordException(BaseDomainException):
    def __init__(self) -> None:
        super().__init__(detail="Wrong password")


class ForbiddenException(BaseDomainException):
    def __init__(self) -> None:
        super().__init__(detail="You have not needed permissions to do this")
