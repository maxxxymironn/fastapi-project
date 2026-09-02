from app.infrastucture.database import db
from app.infrastucture.repositories.location import LocationRepository
from app.schemas.location import ResponseLocationSchema


class GetLocationListUseCase:
    def __init__(self):
        self._db = db
        self._repo = LocationRepository()

    async def execute(self) -> list[ResponseLocationSchema]:
        with self._db.session() as session:
            location_list = await self._repo.get_list(session)

        return [
            ResponseLocationSchema.model_validate(location)
            for location in location_list
        ]
