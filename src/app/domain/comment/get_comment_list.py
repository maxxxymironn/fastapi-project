from app.schemas.comment import ResponseCommentSchema
from app.infrastucture.database import db
from app.infrastucture.repositories.comment import CommentRepository


class GetCommentListUseCase:
    def __init__(self):
        self._db = db
        self._repo = CommentRepository()

    def execute(self, comment_id: int) -> list[ResponseCommentSchema]:
        with self._db.session() as session:
            comment_list = self._repo.get_comment_list(session, comment_id)

        return [ResponseCommentSchema.model_validate(comment) for comment in comment_list]