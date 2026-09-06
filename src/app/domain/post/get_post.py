from app.core.exceptions.database_exception import EntityNotFoundException
from app.core.exceptions.post_domain import PostNotFoundByIdException
from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.post import PostRepository
from app.schemas.post import ResponsePostSchema


class GetPostByTitleUseCase:
    def __init__(self):
        self._db = db
        self._repo = PostRepository()

    async def execute(self, id: int) -> ResponsePostSchema:
        try:
            async with self._db.session() as session:
                post = await self._repo.get_post_by_id(session, id)
        except EntityNotFoundException:
            raise PostNotFoundByIdException(id)

        return ResponsePostSchema.model_validate(post)
