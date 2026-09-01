from app.infrastucture.database import db
from app.infrastucture.repositories.post import PostRepository
from app.schemas.post import ResponsePostSchema


class GetPostByTitleUseCase:
    def __init__(self):
        self._db = db
        self._repo = PostRepository()

    async def execute(self, id: int):
        with self._db.session() as session:
            post = await self._repo.get_post_by_id(session, id)

        return ResponsePostSchema.model_validate(post)
