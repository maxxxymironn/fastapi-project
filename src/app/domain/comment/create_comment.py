from app.infrastucture.database import db
from app.infrastucture.repositories.comment import CommentRepository
from app.schemas.comment import CreateCommentSchema, ResponseCommentSchema


class CreateCommentUseCase:
    def __init__(self):
        self._db = db
        self._repo = CommentRepository()

    async def execute(
        self, post_id: int, comment_data: CreateCommentSchema
    ) -> ResponseCommentSchema:
        with self._db.session() as session:
            comment = await self._repo.create_comment(session, post_id, comment_data)

        return ResponseCommentSchema.model_validate(comment)
