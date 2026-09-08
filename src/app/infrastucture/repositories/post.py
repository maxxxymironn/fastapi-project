from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions.database_exception import (
    EntityListException,
    EntityNotCreatedException,
    EntityNotDeletedException,
    EntityNotFoundException,
)
from app.infrastucture.models.post import PostModel
from app.schemas.post import CreatePostSchema, EditPostSchema


class PostRepository:
    def __init__(self):
        self._model = PostModel

    async def get_post_by_id(self, session: AsyncSession, id: int) -> PostModel:
        query = (
            select(self._model)
            .where(self._model.id == id, self._model.is_published)
            .options(
                selectinload(self._model.author),
                selectinload(self._model.comments)
            )
        )

        post: PostModel | None = await session.scalar(query)

        if not post:
            raise EntityNotFoundException()

        return post

    async def get_post_list(self, session: AsyncSession):
        query = (
            select(self._model)
            .where(self._model.is_published)
            .options(
                selectinload(self._model.author),
                selectinload(self._model.comments)
            )
        )

        try:
            return (await session.scalars(query)).all()
        except IntegrityError:
            raise EntityListException()

    async def get_post_list_by_category(
        self, session: AsyncSession, category_slug: str
    ):
        query = (
            select(self._model)
            .where(self._model.category_slug == category_slug, self._model.is_published)
            .options(
                selectinload(self._model.author),
                selectinload(self._model.comments)
            )
        )

        try:
            return (await session.scalars(query)).all()
        except IntegrityError:
            raise EntityListException()

    async def get_post_list_by_location(
        self, session: AsyncSession, location_name: str
    ):
        query = (
            select(self._model)
            .where(self._model.location_name == location_name, self._model.is_published)
            .options(
                selectinload(self._model.author),
                selectinload(self._model.comments)
            )
        )

        try:
            return (await session.scalars(query)).all()
        except IntegrityError:
            raise EntityListException()

    async def get_post_list_by_category_and_location(
        self, session: AsyncSession, category_slug: str, location_name: str
    ):
        query = (
            select(self._model)
            .where(
                self._model.location_name == location_name,
                self._model.category_slug == category_slug,
                self._model.is_published
            )
            .options(
                selectinload(self._model.author),
                selectinload(self._model.comments)
            )
        )

        try:
            return (await session.scalars(query)).all()
        except IntegrityError:
            raise EntityListException()

    async def create_post(
        self, session: AsyncSession, author_username: str, post_data: CreatePostSchema
    ) -> PostModel:
        values_dict = post_data.model_dump(exclude_none=True, exclude_unset=True)
        values_dict.update({"author_username": author_username})
        print(values_dict)

        query = (
            insert(self._model)
            .values(values_dict)
            .returning(self._model)
            .options(
                selectinload(self._model.author),
                selectinload(self._model.comments)
            )
        )

        try:
            post: PostModel = await session.scalar(query)
        except IntegrityError:
            raise EntityNotCreatedException()

        return post

    async def update_post(
        self, session: AsyncSession, id: int, post_data: EditPostSchema
    ) -> PostModel:
        query = (
            update(self._model)
            .where(self._model.id == id)
            .values(post_data.model_dump(exclude_none=True, exclude_unset=True))
            .returning(self._model)
            .options(
                selectinload(self._model.author),
                selectinload(self._model.comments)
            )
        )

        try:
            post: PostModel | None = await session.scalar(query)
        except IntegrityError:
            raise EntityNotCreatedException()

        if not post:
            raise EntityNotFoundException()

        return post

    async def delete_post(self, session: AsyncSession, id: int) -> None:
        query = (
            delete(self._model)
            .where(self._model.id == id)
            .returning(self._model)
        )

        try:
            is_deleted: bool = await session.scalar(query) is not None
        except IntegrityError:
            raise EntityNotDeletedException()

        if not is_deleted:
            raise EntityNotFoundException()
