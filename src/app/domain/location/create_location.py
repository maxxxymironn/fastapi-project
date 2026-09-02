from app.infrastucture.database import db
from app.infrastucture.repositories.location import LocationRepository
from app.schemas.location import CreateLocationSchema, ResponseLocationSchema


class CreateLocationUseCase:
    def __init__(self):
        self._db = db
        self._repo = LocationRepository()

    async def execute(
        self, location_data: CreateLocationSchema
    ) -> ResponseLocationSchema:
        with self._db.session() as session:
            location = await self._repo.create(session, location_data)

        return ResponseLocationSchema.model_validate(location)
