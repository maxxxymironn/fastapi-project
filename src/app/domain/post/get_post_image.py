from fastapi.responses import FileResponse

from app.core.exceptions.database_exception import EntityNotFoundException
from app.core.exceptions.file_domain_exceptions import NoImageException
from app.core.exceptions.post_domain_exception import PostNotFoundByIdException
from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.post import PostRepository


class GetPostImageByIdUseCase:
    def __init__(self):
        self._db = db
        self._repo = PostRepository()
        self._image_folder = "./images"

    async def execute(self, id: int) -> FileResponse:
        try:
            async with self._db.session() as session:
                post = await self._repo.get_post_by_id(session, id)
        except EntityNotFoundException:
            raise PostNotFoundByIdException(id)

        if not post.image_path:
            raise NoImageException

        full_image_path: str = f"{self._image_folder}/{post.image_path}.jpeg"
        return FileResponse(full_image_path, media_type="image/jpeg")
