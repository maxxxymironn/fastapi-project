from app.infrastucture.database import db
from app.schemas.comment import EditCommentSchema, ResponseCommentSchema
from app.infrastucture.repositories.comment import CommentRepository


class EditCommentUseCase:
    def __init__(self):
        self._db = db
        self._repo = CommentRepository()

    def execute(self, post_id: int, user_id: int, comment_id: int, comment_data: EditCommentSchema) -> ResponseCommentSchema:
        with self._db.session() as session:
            comment = self._repo.edit_comment(session, post_id, user_id, comment_id, comment_data)

        return ResponseCommentSchema.model_validate(comment)