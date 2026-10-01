from fastapi import UploadFile

from app.core.exceptions.comment_domain_exception import CommentNotCreatedException
from app.core.exceptions.database_exception import EntityNotCreatedException
from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.comment import CommentRepository
from app.schemas.comment import ResponseCommentSchema
from app.services.get_image_name import get_image_name


class CreateCommentUseCase:
    def __init__(self):
        self._db = db
        self._repo = CommentRepository()

    async def execute(
        self, post_id: int, user_id: int, comment_text: str, image: UploadFile | None
    ) -> ResponseCommentSchema:
        image_path: str | None = get_image_name(image)

        try:
            async with self._db.session() as session:
                comment = await self._repo.create_comment(
                    session, post_id, user_id, comment_text, image_path
                )
        except EntityNotCreatedException:
            raise CommentNotCreatedException()

        return ResponseCommentSchema.model_validate(comment)
