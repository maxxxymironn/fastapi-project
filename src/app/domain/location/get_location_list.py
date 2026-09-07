from app.core.exceptions.database_exception import EntityListException
from app.core.exceptions.location_domain_exception import GetLocationListException
from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.location import LocationRepository
from app.schemas.location import ResponseLocationSchema


class GetLocationListUseCase:
    def __init__(self):
        self._db = db
        self._repo = LocationRepository()

    async def execute(self) -> list[ResponseLocationSchema]:
        try:
            async with self._db.session() as session:
                location_list = await self._repo.get_list(session)
        except EntityListException:
            raise GetLocationListException()

        return [
            ResponseLocationSchema.model_validate(location)
            for location in location_list
        ]
