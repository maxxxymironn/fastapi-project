from app.infrastucture.database import db
from app.infrastucture.repositories.location import LocationRepository
from app.schemas.location import ResponseLocationSchema


class GetLocationUseCase:
    def __init__(self):
        self._db = db
        self._repo = LocationRepository()

    async def execute(self, location_name: str) -> ResponseLocationSchema:
        with self._db.session() as session:
            location = await self._repo.get(session, location_name)

        return ResponseLocationSchema.model_validate(location)
