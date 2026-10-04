from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import SecretStr

from app.core.exceptions.auth_exception import CredentialsException
from app.core.exceptions.user_domain_exception import UserNotFoundByUsernameException
from app.infrastucture.postgresql.database import Database, db
from app.infrastucture.repositories.user import UserRepository
from app.schemas.user import ResponseUserSchema

SECRET_AUTH_KEY = SecretStr(
    "573ca9b083ed10f3b965623838c6c1f8c9082b360bb40755d3a54c47318d8f0b"
)
AUTH_ALGORITHM = "HS256"
AUTH_ERROR_DEATIL = "Невозможно проверить данные авторизации"


class AuthService:
    @staticmethod
    async def get_current_user(
        token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))]
    ):
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
                raise CredentialsException(AUTH_ERROR_DEATIL)
        except JWTError:
            raise CredentialsException(AUTH_ERROR_DEATIL)

        try:
            async with _db.session() as session:
                user = _repo.get_user(session=session, username=username)
                pass
        except UserNotFoundByUsernameException:
            raise CredentialsException(AUTH_ERROR_DEATIL)

        return ResponseUserSchema.model_validate(obj=user)
