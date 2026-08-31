from app.schemas.comment import CreateCommentSchema
from app.schemas.comment import ResponseCommentSchema
from app.infrastucture.database import db
from app.infrastucture.repositories.comment import CommentRepository


class CreateCommentUseCase:
    def __init__(self):
        self._db = db
        self._repo = CommentRepository()

    def execute(self, post_id: int, comment_data: CreateCommentSchema) -> ResponseCommentSchema:
        with self._db.session() as session:
            comment = self._repo.create_comment(session, post_id, comment_data)

        return ResponseCommentSchema.model_validate(comment)