from app.core.exceptions.comment_domain_exception import (
    CommentNotDeletedException,
    CommentNotFoundException,
)
from app.core.exceptions.database_exception import (
    EntityNotDeletedException,
    EntityNotFoundException,
)
from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.comment import CommentRepository


class DeleteCommentUseCase:
    def __init__(self):
        self._db = db
        self._repo = CommentRepository()

    async def execute(self, post_id: int, user_id: int, comment_id: int) -> None:
        try:
            async with self._db.session() as session:
                await self._repo.delete_comment(session, post_id, user_id, comment_id)
        except EntityNotDeletedException:
            raise CommentNotDeletedException(comment_id)
        except EntityNotFoundException:
            raise CommentNotFoundException(comment_id)
