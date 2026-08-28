from sqlalchemy.orm import Session

from app.infrastucture.database import db
from app.infrastucture.repositories.user import UserRepository
from app.schemas.user import BaseUserSchema, ResponseUserSchema


class UpdateUserAttributesUseCase:
    def __init__(self):
        self._db = db
        self._repo = UserRepository()

    def execute(self, new_user_data: BaseUserSchema)-> ResponseUserSchema:
        with self._db.session() as session:
            user = self._repo.update_user_attributes(session, new_user_data)

        return ResponseUserSchema.model_validate(obj=user)