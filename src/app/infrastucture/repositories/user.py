from sqlalchemy import update
from fastapi import HTTPException, status

from sqlalchemy import select, insert
from sqlalchemy.orm import Session

from app.infrastucture.models.user import UserModel
from app.schemas.user import CreateUserSchema, BaseUserSchema


class UserRepository:
    def __init__(self):
        self._model = UserModel

    def create_user(self, session: Session, user_data: CreateUserSchema) -> UserModel:
        query = (
            insert(self._model)
            .values(user_data.model_dump())
            .returning(self._model)
        )

        try:
            created_user = session.scalar(query)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user with username = {user_data.username} already exist"
            )
        return created_user


    def get_user(self, session: Session, username: str) -> UserModel:
        query = (
            select(self._model)
            .where(self._model.username == username)
        )

        user: UserModel | None = session.scalar(query)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return user
    

    def update_user_attributes(self, session: Session, new_user_data: BaseUserSchema) -> UserModel:
        query = (
            update(self._model)
            .where(self._model.username == new_user_data.username)
            .values(
                first_name=new_user_data.first_name,
                last_name=new_user_data.last_name,
                email=new_user_data.email
            ).returning(self._model)
        )

        user = session.scalar(query)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return user
