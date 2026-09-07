from app.core.exceptions.database_exception import EntityAlreadyExistsException
from app.core.exceptions.location_domain_exception import LocationAlreadyExistsException
from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.location import LocationRepository
from app.schemas.location import CreateLocationSchema, ResponseLocationSchema


class CreateLocationUseCase:
    def __init__(self):
        self._db = db
        self._repo = LocationRepository()

    async def execute(
        self, location_data: CreateLocationSchema
    ) -> ResponseLocationSchema:
        try:
            async with self._db.session() as session:
                location = await self._repo.create(session, location_data)
        except EntityAlreadyExistsException:
            raise LocationAlreadyExistsException(location_name=location_data.name)

        return ResponseLocationSchema.model_validate(location)
