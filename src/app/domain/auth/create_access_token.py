from datetime import datetime, timedelta, timezone

from jose import jwt

from app.services.auth import AUTH_ALGORITHM, SECRET_AUTH_KEY


class CreateAccessTokenUseCase:
    def __init__(self, token_expire_minutes: int = 5) -> None:
        self._ACCESS_TOKEN_EXPIRE_MINUTES = token_expire_minutes

    async def execute(self, login: str, expires_delta: timedelta | None = None) -> str:
        to_encode: dict[str, str | datetime] = {"sub": login}

        expire = datetime.now(timezone.utc)
        if expires_delta:
            expire += expires_delta
        else:
            expire += timedelta(minutes=self._ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            claims=to_encode,
            key=SECRET_AUTH_KEY.get_secret_value(),
            algorithm=AUTH_ALGORITHM
        )

        return encoded_jwt
