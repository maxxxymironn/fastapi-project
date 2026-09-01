from fastapi import HTTPException, status
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session

from app.infrastucture.models.post import PostModel
from app.schemas.post import CreatePostSchema, EditPostSchema


class PostRepository:
    def __init__(self):
        self._model = PostModel

    async def get_post_by_id(self, session: Session, id: int) -> PostModel:
        query = select(self._model).where(self._model.id == id)

        post = session.scalar(query)

        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return post

    async def get_post_list(self, session: Session):
        query = select(self._model)
        return session.scalars(query).all()

    async def get_post_list_by_category(self, session: Session, category_slug: str):
        query = select(self._model).where(self._model.category_slug == category_slug)
        post_list = session.scalars(query).all()

        return post_list

    async def create_post(
        self, session: Session, post_data: CreatePostSchema
    ) -> PostModel:
        query = (
            insert(self._model)
            .values(post_data.model_dump(exclude_none=True, exclude_unset=True))
            .returning(self._model)
        )

        try:
            post = session.scalar(query)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        return post

    async def update_post(
        self, session: Session, id: int, post_data: EditPostSchema
    ) -> PostModel:
        query = (
            update(self._model)
            .where(self._model.id == id)
            .values(post_data.model_dump(exclude_none=True, exclude_unset=True))
            .returning(self._model)
        )

        try:
            post = session.scalar(query)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        return post

    async def delete_post(self, session: Session, id: int) -> None:
        query = delete(self._model).where(self._model.id == id).returning(self._model)

        try:
            is_deleted = session.scalar(query) is not None
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        if not is_deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
