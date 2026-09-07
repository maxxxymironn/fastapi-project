from app.core.exceptions.database_exception import (
    EntityNotCreatedException,
    EntityNotFoundException,
)
from app.core.exceptions.post_domain_exception import (
    PostNotCreatedException,
    PostNotFoundByIdException,
)
from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.post import PostRepository
from app.schemas.post import EditPostSchema, ResponsePostSchema


class EditPostUseCase:
    def __init__(self):
        self._db = db
        self._repo = PostRepository()

    async def execute(self, id: int, post_data: EditPostSchema) -> ResponsePostSchema:
        try:
            async with self._db.session() as session:
                post = await self._repo.update_post(session, id, post_data)
        except EntityNotFoundException:
            raise PostNotFoundByIdException(id)
        except EntityNotCreatedException:
            raise PostNotCreatedException(
                category_slug=post_data.category_slug,
                location_name=post_data.location_name
            )

        return ResponsePostSchema.model_validate(post)
