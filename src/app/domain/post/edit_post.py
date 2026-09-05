from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.post import PostRepository
from app.schemas.post import EditPostSchema, ResponsePostSchema


class EditPostUseCase:
    def __init__(self):
        self._db = db
        self._repo = PostRepository()

    async def execute(self, id: int, user_data: EditPostSchema) -> ResponsePostSchema:
        async with self._db.session() as session:
            post = await self._repo.update_post(session, id, user_data)

        return ResponsePostSchema.model_validate(post)
