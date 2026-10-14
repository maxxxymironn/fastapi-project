from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions.database_exception import (
    EntityNotCreatedException,
    EntityNotFoundException,
)
from app.infrastucture.models.user import UserModel


class AuthRepository:
    def __init__(self):
        self._model = UserModel

    async def save_refresh_token(
        self, session: AsyncSession, username: str, hashed_token: str
    ) -> None:
        query = (
            update(self._model)
            .where(self._model.username == username)
            .values(hashed_refresh_token=hashed_token)
            .returning(self._model.hashed_refresh_token)
        )

        token: str | None = await session.scalar(query)
        if not token:
            raise EntityNotCreatedException()

    async def get_refresh_token(self, session: AsyncSession, username: str) -> str:
        query = (
            select(self._model.hashed_refresh_token)
            .where(self._model.username == username)
        )

        token: str | None = await session.scalar(query)
        if not token:
            raise EntityNotFoundException()

        return token
