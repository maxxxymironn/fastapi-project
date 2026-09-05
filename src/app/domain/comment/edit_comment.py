from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.comment import CommentRepository
from app.schemas.comment import EditCommentSchema, ResponseCommentSchema


class EditCommentUseCase:
    def __init__(self):
        self._db = db
        self._repo = CommentRepository()

    async def execute(
        self,
        post_id: int,
        user_id: int,
        comment_id: int,
        comment_data: EditCommentSchema,
    ) -> ResponseCommentSchema:
        async with self._db.session() as session:
            comment = await self._repo.edit_comment(
                session, post_id, user_id, comment_id, comment_data
            )

        return ResponseCommentSchema.model_validate(comment)
