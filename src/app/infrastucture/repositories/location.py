from sqlalchemy import delete, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions.database_exception import (
    EntityAlreadyExistsException,
    EntityListException,
    EntityNotDeletedException,
    EntityNotFoundException,
)
from app.infrastucture.models.location import LocationModel
from app.schemas.location import CreateLocationSchema


class LocationRepository:
    def __init__(self):
        self._model = LocationModel

    async def get_list(self, session: AsyncSession):
        query = (
            select(self._model)
            .where(self._model.is_published)
        )

        try:
            return (await session.scalars(query)).all()
        except IntegrityError:
            raise EntityListException()

    async def get(self, session: AsyncSession, location_name: str) -> LocationModel:
        query = (
            select(self._model)
            .where(self._model.name == location_name)
        )

        location: LocationModel | None = await session.scalar(query)
        if not location:
            raise EntityNotFoundException()

        return location

    async def create(
        self, session: AsyncSession, location_data: CreateLocationSchema
    ) -> LocationModel:
        query = (
            insert(self._model)
            .values(location_data.model_dump())
            .returning(self._model)
        )

        try:
            location: LocationModel = await session.scalar(query)
        except IntegrityError:
            raise EntityAlreadyExistsException()

        return location

    async def delete(self, session: AsyncSession, location_name: str) -> None:
        query = (
            delete(self._model)
            .where(self._model.name == location_name)
            .returning(self._model)
        )

        try:
            location: LocationModel | None = await session.scalar(query)
        except IntegrityError:
            raise EntityNotDeletedException()

        if not location:
            raise EntityNotFoundException()
