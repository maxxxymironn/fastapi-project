from datetime import datetime, timedelta, timezone

from jose import exceptions, jwt

from app.core.config import settings
from app.core.exceptions.auth_domain_exception import TokenNotCreatedException
from app.core.exceptions.database_exception import (
    EntityNotCreatedException,
    EntityNotFoundException,
)
from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.auth import AuthRepository
from app.schemas.auth import RefreshTokenSchema


class RefreshTokensUseCase:
    def __init__(self):
        self._db = db
        self._repo = AuthRepository()

    async def execute(self, refresh_token: RefreshTokenSchema) -> tuple[str, str]:
        try:
            jwt_token = jwt.decode(
                token=refresh_token.refresh_token,
                key=settings.SECRET_AUTH_KEY.get_secret_value(),
                algorithms=[settings.AUTH_ALGORITHM]
            )
            # if jwt_token.get("type") != "refresh":
            #     raise TokenNotCreatedException()
            username: str = jwt_token.get("sub")
        except exceptions.JWTError:
            raise TokenNotCreatedException()

        try:
            async with self._db.session() as session:
                saved_refresh_token: str = await self._repo.get_refresh_token(
                    session, username
                )
                if saved_refresh_token != refresh_token.refresh_token:
                    raise EntityNotFoundException
        except EntityNotFoundException:
            raise TokenNotCreatedException()

        access_token_to_encode: dict[str, str | datetime] = {"sub": username}
        refresh_token_to_encode: dict[str, str | datetime] = {"sub": username}

        token_expire = datetime.now(timezone.utc)
        access_token_expire = token_expire + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        refresh_token_expire = token_expire + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )

        access_token_to_encode.update({"exp": access_token_expire})
        refresh_token_to_encode.update({"exp": refresh_token_expire})

        access_token_encoded_jwt = jwt.encode(
            claims=access_token_to_encode,
            key=settings.SECRET_AUTH_KEY.get_secret_value(),
            algorithm=settings.AUTH_ALGORITHM
        )
        refresh_token_encoded_jwt = jwt.encode(
            claims=refresh_token_to_encode,
            key=settings.SECRET_AUTH_KEY.get_secret_value(),
            algorithm=settings.AUTH_ALGORITHM
        )

        try:
            async with self._db.session() as session:
                await self._repo.save_refresh_token(
                    session, username, refresh_token_encoded_jwt
                )
        except EntityNotCreatedException:
            raise TokenNotCreatedException()

        return access_token_encoded_jwt, refresh_token_encoded_jwt
