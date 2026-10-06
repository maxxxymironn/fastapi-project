from app.core.exceptions.auth_exception import ForbiddenException
from app.core.exceptions.database_exception import (
    EntityNotDeletedException,
    EntityNotFoundException,
)
from app.core.exceptions.post_domain_exception import (
    PostNotDeletedException,
    PostNotFoundByIdException,
)
from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.post import PostRepository


class DeletePostUseCase:
    def __init__(self):
        self._db = db
        self._repo = PostRepository()

    async def execute(self, post_id: int, username: str, is_user_admin: bool) -> None:
        try:
            async with self._db.session() as session:
                post = await self._repo.get_post_by_id(session, post_id)
                if post.author_username != username and not is_user_admin:
                    raise ForbiddenException()

                await self._repo.delete_post(session, post_id)
        except EntityNotDeletedException:
            raise PostNotDeletedException(post_id)
        except EntityNotFoundException:
            raise PostNotFoundByIdException(post_id)
