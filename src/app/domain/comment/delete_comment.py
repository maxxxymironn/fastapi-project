from app.infrastucture.database import db
from app.infrastucture.repositories.comment import CommentRepository


class DeleteCommentUseCase:
    def __init__(self):
        self._db = db
        self._repo = CommentRepository()

    async def execute(self, post_id: int, user_id: int, comment_id) -> None:
        with self._db.session() as session:
            await self._repo.delete_comment(session, post_id, user_id, comment_id)
