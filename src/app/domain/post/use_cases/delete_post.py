from app.infrastucture.repositories.post import PostRepository
from app.infrastucture.database import db


class DeletePostUseCase:
    def __init__(self):
        self._db = db
        self._repo = PostRepository()

    async def execute(self, id: int):
        with self._db.session() as session:
            return await self._repo.delete_post(session, id)
            