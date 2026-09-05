from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.post import PostRepository


class DeletePostUseCase:
    def __init__(self):
        self._db = db
        self._repo = PostRepository()

    async def execute(self, id: int):
        async with self._db.session() as session:
            await self._repo.delete_post(session, id)
