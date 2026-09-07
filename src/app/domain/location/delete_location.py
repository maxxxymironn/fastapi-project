from app.core.exceptions.database_exception import (
    EntityNotDeletedException,
    EntityNotFoundException,
)
from app.core.exceptions.location_domain_exception import (
    LocationNotDeletedException,
    LocationNotFoundException,
)
from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.location import LocationRepository


class DeleteLocationUseCase:
    def __init__(self):
        self._db = db
        self._repo = LocationRepository()

    async def execute(self, location_name: str) -> None:
        location_name = location_name.lower()
        try:
            async with self._db.session() as session:
                await self._repo.delete(session, location_name)
        except EntityNotDeletedException:
            raise LocationNotDeletedException(location_name=location_name)
        except EntityNotFoundException:
            raise LocationNotFoundException(location_name=location_name)
