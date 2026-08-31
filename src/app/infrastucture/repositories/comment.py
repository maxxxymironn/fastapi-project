from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session
from fastapi import status, HTTPException

from app.schemas.comment import EditCommentSchema, CreateCommentSchema
from app.infrastucture.models.comment import CommentModel


class CommentRepository:
    def __init__(self):
        self._model = CommentModel

    def get_comment_list(self, session: Session, post_id: int):
        query = (
            select(self._model)
            .where(self._model.post_id == post_id)
        )

        return session.scalars(query).all()

    def create_comment(
        self, 
        session: Session, 
        post_id: int, 
        comment_data: CreateCommentSchema
    ) -> CommentModel:
        query = (
            insert(self._model)
            .values(comment_data.model_dump() | {"post_id": post_id})
            .returning(self._model)
        )

        try:
            comment = session.scalar(query)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        return comment

    def edit_comment(
        self,
        session: Session,
        post_id: int,
        user_id: int,
        comment_id: int,
        comment_data: EditCommentSchema
    ) -> CommentModel:
        query = (
            update(self._model)
            .values(comment_data.model_dump())
            .where(
                self._model.id == comment_id,
                self._model.post_id == post_id,
                self._model.author_id == user_id)
            .returning(self._model)
        )

        try:
            comment = session.scalar(query)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        if not comment:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        return comment

    def delete_comment(self, session, post_id, user_id, comment_id) -> None:
        query = (
            delete(self._model)
            .where(
                self._model.id == comment_id,
                self._model.post_id == post_id,
                self._model.author_id == user_id)
            .returning(self._model)
        )

        try:
            is_deleted = session.scalar(query) is not None
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        
        if not is_deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
