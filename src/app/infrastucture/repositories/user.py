from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions.database import (
    DeleteEntityException,
    EntityAlreadyExistsException,
    EntityListException,
    EntityNotFoundException,
)
from app.infrastucture.models.user import UserModel
from app.schemas.user import CreateUserSchema, EditUserSchema


class UserRepository:
    def __init__(self):
        self._model = UserModel

    async def get_user(self, session: AsyncSession, username: str) -> UserModel:
        query = (
            select(self._model)
            .options(selectinload(self._model.posts))
            .where(self._model.username == username)
        )

        user: UserModel | None = await session.scalar(query)
        if not user:
            raise EntityNotFoundException()

        return user

    async def get_user_list(self, session: AsyncSession):
        query = (
            select(self._model)
            .options(selectinload(self._model.posts))
        )

        try:
            post_list = (await session.scalars(query)).all()
        except IntegrityError:
            raise EntityListException

        return post_list

    async def create_user(
        self, session: AsyncSession, user_data: CreateUserSchema
    ) -> UserModel:
        query = (
            insert(self._model)
            .values(user_data.model_dump())
            .returning(self._model)
            .options(selectinload(self._model.posts))
        )

        try:
            user: UserModel = await session.scalar(query)
        except IntegrityError:
            raise EntityAlreadyExistsException()

        return user

    async def update_user_attributes(
        self, session: AsyncSession, username: str, user_data: EditUserSchema
    ) -> UserModel:
        query = (
            update(self._model)
            .where(self._model.username == username)
            .values(user_data.model_dump(exclude_none=True, exclude_unset=True))
            .returning(self._model)
            .options(selectinload(self._model.posts))
        )

        try:
            user: UserModel | None = await session.scalar(query)
        except IntegrityError:
            raise EntityAlreadyExistsException()
        if not user:
            raise EntityNotFoundException()

        return user

    async def delete_user(self, session: AsyncSession, username: str) -> None:
        query = (
            delete(self._model)
            .where(self._model.username == username)
            .returning(self._model)
        )

        try:
            is_deleted: bool = await session.scalar(query) is not None
        except IntegrityError:
            raise DeleteEntityException()

        if not is_deleted:
            raise EntityNotFoundException()
