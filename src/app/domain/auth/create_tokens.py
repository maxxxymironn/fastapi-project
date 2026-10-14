from datetime import datetime, timedelta, timezone

from jose import jwt

from app.core.config import settings
from app.core.exceptions.auth_domain_exception import TokenNotCreatedException
from app.core.exceptions.database_exception import EntityNotCreatedException
from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.auth import AuthRepository


class CreateTokensUseCase:
    def __init__(self):
        self._db = db
        self._repo = AuthRepository()

    async def execute(self, login: str) -> tuple[str, str]:
        access_token_to_encode: dict[str, str | datetime] = {"sub": login}
        refresh_token_to_encode: dict[str, str | datetime] = {"sub": login}

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
                    session, login, refresh_token_encoded_jwt
                )
        except EntityNotCreatedException:
            raise TokenNotCreatedException()

        return access_token_encoded_jwt, refresh_token_encoded_jwt
