from app.core.exceptions.database_exception import (
    EntityNotCreatedException,
    EntityNotFoundException,
)
from app.core.exceptions.post_domain_exception import PostNotCreatedException
from app.core.exceptions.user_domain_exception import UserNotFoundByUsernameException
from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.post import PostRepository
from app.infrastucture.repositories.user import UserRepository
from app.schemas.post import CreatePostSchema, ResponsePostSchema


class CreatePostUseCase:
    def __init__(self):
        self._db = db
        self._repo = PostRepository()
        self._user_repo = UserRepository()

    async def execute(
        self, author_username: str, post_data: CreatePostSchema
    ) -> ResponsePostSchema:
        try:
            async with self._db.session() as session:
                await self._user_repo.get_user(session, author_username)

                post = await self._repo.create_post(session, author_username, post_data)
        except EntityNotCreatedException:
            raise PostNotCreatedException(
                category_slug=post_data.category_slug,
                location_name=post_data.location_name,
            )
        except EntityNotFoundException:
            raise UserNotFoundByUsernameException(
                author_username
            )

        return ResponsePostSchema.model_validate(post)
