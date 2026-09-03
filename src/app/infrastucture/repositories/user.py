from fastapi import HTTPException, status
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session

from app.infrastucture.models.user import UserModel
from app.schemas.post import ResponsePostSchema
from app.schemas.user import CreateUserSchema, EditUserSchema


class UserRepository:
    def __init__(self):
        self._model = UserModel

    async def is_user_exist(self, session: Session, username: str) -> bool:
        query = (
            select(
                select(self._model)
                .where(self._model.username == username)
                .exists()
            )
        )

        return session.scalar(query) or False

    async def get_user(self, session: Session, username: str) -> UserModel:
        query = select(self._model).where(self._model.username == username)

        user: UserModel | None = session.scalar(query)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        print([ResponsePostSchema.model_validate(post) for post in user.posts])
        return user

    async def create_user(
        self, session: Session, user_data: CreateUserSchema
    ) -> UserModel:
        query = (
            insert(self._model).values(user_data.model_dump()).returning(self._model)
        )

        try:
            created_user = session.scalar(query)
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user with username = {user_data.username} already exist",
            )
        return created_user

    async def update_user_attributes(
        self, session: Session, username: str, user_data: EditUserSchema
    ) -> UserModel:
        query = (
            update(self._model)
            .where(self._model.username == username)
            .values(user_data.model_dump(exclude_none=True, exclude_unset=True))
            .returning(self._model)
        )

        user = session.scalar(query)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return user

    async def delete_user(self, session: Session, username: str) -> None:
        query = (
            delete(self._model)
            .where(self._model.username == username)
            .returning(self._model)
        )

        try:
            was_user_exist: bool = session.scalar(query) is not None
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        if not was_user_exist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
