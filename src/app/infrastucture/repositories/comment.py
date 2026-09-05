from fastapi import HTTPException, status
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastucture.models.comment import CommentModel
from app.schemas.comment import CreateCommentSchema, EditCommentSchema


class CommentRepository:
    def __init__(self):
        self._model = CommentModel

    async def get_comment_list(self, session: AsyncSession, post_id: int):
        query = select(self._model).where(self._model.post_id == post_id)

        return (await session.scalars(query)).all()

    async def create_comment(
        self, session: AsyncSession, post_id: int, comment_data: CreateCommentSchema
    ) -> CommentModel:
        query = (
            insert(self._model)
            .values(comment_data.model_dump() | {"post_id": post_id})
            .returning(self._model)
        )

        try:
            comment: CommentModel | None = await session.scalar(query)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        return comment

    async def edit_comment(
        self,
        session: AsyncSession,
        post_id: int,
        user_id: int,
        comment_id: int,
        comment_data: EditCommentSchema,
    ) -> CommentModel:
        query = (
            update(self._model)
            .values(comment_data.model_dump())
            .where(
                self._model.id == comment_id,
                self._model.post_id == post_id,
                self._model.author_id == user_id,
            )
            .returning(self._model)
        )

        try:
            comment: CommentModel | None = await session.scalar(query)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        if not comment:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        return comment

    async def delete_comment(self, session, post_id, user_id, comment_id) -> None:
        query = (
            delete(self._model)
            .where(
                self._model.id == comment_id,
                self._model.post_id == post_id,
                self._model.author_id == user_id,
            )
            .returning(self._model)
        )

        try:
            is_deleted: bool = await session.scalar(query) is not None
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        if not is_deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
