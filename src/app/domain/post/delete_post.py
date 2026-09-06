from app.core.exceptions.database_exception import (
    EntityNotDeletedException,
    EntityNotFoundException,
)
from app.core.exceptions.post_domain import (
    PostNotDeletedException,
    PostNotFoundByIdException,
)
from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.post import PostRepository


class DeletePostUseCase:
    def __init__(self):
        self._db = db
        self._repo = PostRepository()

    async def execute(self, id: int) -> None:
        try:
            async with self._db.session() as session:
                await self._repo.delete_post(session, id)
        except EntityNotDeletedException:
            raise PostNotDeletedException(id)
        except EntityNotFoundException:
            raise PostNotFoundByIdException(id)
