from fastapi.responses import FileResponse

from app.core.exceptions.comment_domain_exception import CommentNotFoundException
from app.core.exceptions.database_exception import EntityNotFoundException
from app.core.exceptions.file_domain_exceptions import NoImageException
from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.comment import CommentRepository


class GetCommentImageByIdUseCase:
    def __init__(self):
        self._db = db
        self._repo = CommentRepository()
        self._image_folder = "./images"

    async def execute(self, post_id: int, comment_id: int) -> FileResponse:
        try:
            async with self._db.session() as session:
                comment = await self._repo.get_comment_by_id(
                    session, post_id, comment_id
                )
        except EntityNotFoundException:
            raise CommentNotFoundException(comment_id)

        if not comment.image_path:
            raise NoImageException()

        full_image_path: str = f"{self._image_folder}/{comment.image_path}.jpeg"
        return FileResponse(full_image_path, media_type="image/jpeg")
