from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import SecretStr

from app.core.exceptions.auth_exception import (
    AlreadyAuthenticatedException,
    CredentialsException,
    NotAdminException,
)
from app.core.exceptions.user_domain_exception import UserNotFoundByUsernameException
from app.infrastucture.postgresql.database import Database, db
from app.infrastucture.repositories.user import UserRepository
from app.schemas.user import ResponseUserSchema

SECRET_AUTH_KEY = SecretStr(
    "573ca9b083ed10f3b965623838c6c1f8c9082b360bb40755d3a54c47318d8f0b"
)
AUTH_ALGORITHM = "HS256"
AUTH_ERROR_DETAIL = "Невозможно проверить данные авторизации"


class AuthService:
    @staticmethod
    async def _get_current_user_or_none(
        token: Annotated[str, Depends(
            OAuth2PasswordBearer(tokenUrl="token", auto_error=False)
        )]
    ) -> ResponseUserSchema | None:
        if not token:
            return None

        _db: Database = db
        _repo: UserRepository = UserRepository()

        try:
            payload = jwt.decode(
                token=token,
                key=SECRET_AUTH_KEY.get_secret_value(),
                algorithms=[AUTH_ALGORITHM],
            )

            username: str | None = payload.get("sub")
            if username is None:
                return None
        except JWTError:
            return None

        try:
            async with _db.session() as session:
                user = await _repo.get_user(session=session, username=username)
                pass
        except UserNotFoundByUsernameException:
            return None

        return ResponseUserSchema.model_validate(obj=user)

    @staticmethod
    async def get_current_user(
        user: ResponseUserSchema | None = Depends(_get_current_user_or_none)
    ) -> ResponseUserSchema:
        if not user:
            raise CredentialsException(AUTH_ERROR_DETAIL)
        return user

    @staticmethod
    async def is_anonymous(
        user: ResponseUserSchema | None = Depends(_get_current_user_or_none)
    ) -> None:
        if user:
            raise AlreadyAuthenticatedException()

    @staticmethod
    async def is_admin(
        user: ResponseUserSchema = Depends(get_current_user)
    ) -> ResponseUserSchema:
        if not user.is_admin:
            raise NotAdminException()
        return user
