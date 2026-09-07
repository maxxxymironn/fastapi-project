from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.core.exceptions.database_exception import (
    EntityAlreadyExistsException,
    EntityListException,
    EntityNotDeletedException,
    EntityNotFoundException,
)
from app.infrastucture.models.category import CategoryModel
from app.schemas.category import CreateCategorySchema, EditCategorySchema


class CategoryRepository:
    def __init__(self):
        self._model = CategoryModel

    async def get(self, session: AsyncSession, category_slug: str) -> CategoryModel:
        query = select(self._model).where(self._model.slug == category_slug)

        category: CategoryModel | None = await session.scalar(query)

        if not category:
            raise EntityNotFoundException()

        return category

    async def get_list(self, session: AsyncSession):
        query = select(self._model)

        try:
            category_list = (await session.scalars(query)).all()
        except IntegrityError:
            raise EntityListException()

        return category_list

    async def create(
        self, session: AsyncSession, category_data: CreateCategorySchema
    ) -> CategoryModel:
        query = (
            insert(self._model)
            .values(category_data.model_dump())
            .returning(self._model)
        )

        try:
            category: CategoryModel = await session.scalar(query)
        except IntegrityError:
            raise EntityAlreadyExistsException()

        return category

    async def edit(
        self, session: AsyncSession,
        category_slug: str,
        category_data: EditCategorySchema
    ) -> CategoryModel:
        query = (
            update(self._model)
            .where(self._model.slug == category_slug)
            .values(category_data.model_dump(exclude_none=True, exclude_unset=True))
            .returning(self._model)
        )

        try:
            category: CategoryModel | None = await session.scalar(query)
        except IntegrityError:
            raise EntityAlreadyExistsException()

        if not category:
            raise EntityNotFoundException()

        return category

    async def delete(self, session: AsyncSession, category_slug: str) -> None:
        query = (
            delete(self._model)
            .where(self._model.slug == category_slug)
            .returning(self._model)
        )

        try:
            is_deleted: bool = await session.scalar(query) is not None
        except IntegrityError:
            raise EntityNotDeletedException()

        if not is_deleted:
            raise EntityNotFoundException()
