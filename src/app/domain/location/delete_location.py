from app.infrastucture.database import db
from app.infrastucture.repositories.location import LocationRepository


class DeleteLocationUseCase:
    def __init__(self):
        self._db = db
        self._repo = LocationRepository()

    async def execute(self, location_name: str) -> None:
        with self._db.session() as session:
            await self._repo.delete(session, location_name)
