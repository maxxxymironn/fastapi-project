from fastapi import HTTPException, status
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastucture.models.location import LocationModel
from app.schemas.location import CreateLocationSchema


class LocationRepository:
    def __init__(self):
        self._model = LocationModel

    async def get_list(self, session: AsyncSession):
        query = select(self._model)
        return (await session.scalars(query)).all()

    async def get(self, session: AsyncSession, location_name: str) -> LocationModel:
        query = (
            select(self._model)
            .where(self._model.name == location_name)
        )

        location: LocationModel | None = await session.scalar(query)

        if not location:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
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
            location: LocationModel | None = await session.scalar(query)
        except Exception:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        return location

    async def delete(self, session: AsyncSession, location_name: str) -> None:
        query = (
            delete(self._model)
            .where(self._model.name == location_name)
            .returning(self._model)
        )

        try:
            location: LocationModel | None = await session.scalar(query)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        if not location:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
