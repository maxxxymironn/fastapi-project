from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastucture.models.post import PostModel
from app.schemas.post import CreatePostSchema, EditPostSchema


class PostRepository:
    def __init__(self):
        self._model = PostModel

    async def get_post_by_id(self, session: AsyncSession, id: int) -> PostModel:
        query = (
            select(self._model)
            .where(self._model.id == id)
            .options(selectinload(self._model.author))
        )

        post: PostModel | None = await session.scalar(query)

        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return post

    async def get_post_list(self, session: AsyncSession):
        query = (
            select(self._model)
            .options(selectinload(self._model.author))
        )
        return (await session.scalars(query)).all()

    async def get_post_list_by_category(
        self, session: AsyncSession, category_slug: str
    ):
        query = (
            select(self._model)
            .where(self._model.category_slug == category_slug)
            .options(selectinload(self._model.author))
        )
        return (await session.scalars(query)).all()

    async def create_post(
        self, session: AsyncSession, post_data: CreatePostSchema
    ) -> PostModel:
        query = (
            insert(self._model)
            .values(post_data.model_dump(exclude_none=True, exclude_unset=True))
            .returning(self._model)
            .options(selectinload(self._model.author))
        )

        try:
            post: PostModel | None = await session.scalar(query)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        return post

    async def update_post(
        self, session: AsyncSession, id: int, post_data: EditPostSchema
    ) -> PostModel:
        query = (
            update(self._model)
            .where(self._model.id == id)
            .values(post_data.model_dump(exclude_none=True, exclude_unset=True))
            .returning(self._model)
            .options(selectinload(self._model.author))
        )

        try:
            post: PostModel | None = await session.scalar(query)
        except Exception:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        return post

    async def delete_post(self, session: AsyncSession, id: int) -> None:
        query = (
            delete(self._model)
            .where(self._model.id == id)
            .returning(self._model)
        )

        try:
            is_deleted: bool = await session.scalar(query) is not None
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        if not is_deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
