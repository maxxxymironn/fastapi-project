from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions.database_exception import (
    EntityListException,
    EntityNotCreatedException,
    EntityNotDeletedException,
    EntityNotFoundException,
)
from app.infrastucture.models.comment import CommentModel
from app.infrastucture.models.post import PostModel
from app.schemas.comment import EditCommentSchema


class CommentRepository:
    def __init__(self):
        self._model = CommentModel
        self._post_model = PostModel

    async def get_comment_list(self, session: AsyncSession, post_id: int):
        query = (
            select(self._model)
            .where(
                self._model.post_id == post_id,
                self._model.post.has(self._post_model.is_published.is_(True))
            )
        )

        try:
            return (await session.scalars(query)).all()
        except IntegrityError:
            raise EntityListException()

    async def create_comment(
        self, session: AsyncSession, post_id: int, user_id: int,
        comment_data: EditCommentSchema
    ) -> CommentModel:
        comment_data_dict = comment_data.model_dump()
        comment_data_dict.update({"post_id": post_id, "author_id": user_id})

        query = (
            insert(self._model)
            .values(comment_data_dict)
            .returning(self._model)
        )

        try:
            comment: CommentModel = await session.scalar(query)
        except IntegrityError:
            raise EntityNotCreatedException()

        return comment

    async def edit_comment(
        self, session: AsyncSession, post_id: int, user_id: int,
        comment_id: int, comment_data: EditCommentSchema,
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

        comment: CommentModel | None = await session.scalar(query)

        if not comment:
            raise EntityNotFoundException()

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
        except IntegrityError:
            raise EntityNotDeletedException()

        if not is_deleted:
            raise EntityNotFoundException()
