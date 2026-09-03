from fastapi import HTTPException, status

from app.infrastucture.database import db
from app.infrastucture.repositories.post import PostRepository
from app.infrastucture.repositories.user import UserRepository
from app.schemas.post import CreatePostSchema, ResponsePostSchema


class CreatePostUseCase:
    def __init__(self):
        self._db = db
        self._repo = PostRepository()
        self._user_repo = UserRepository()

    async def execute(self, post_data: CreatePostSchema) -> ResponsePostSchema:
        with self._db.session() as session:
            is_user_exist = await self._user_repo.is_user_exist(
                session, post_data.author_username
            )

            if not is_user_exist:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

            post = await self._repo.create_post(session, post_data)

        return ResponsePostSchema.model_validate(post)
