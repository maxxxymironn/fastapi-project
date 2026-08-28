from sqlalchemy.orm import Session

from app.infrastucture.database import db
from app.infrastucture.repositories.user import UserRepository
from app.schemas.user import ResponseUserSchema


class GetUserByUsernameUseCase:
    def __init__(self):
        self._db = db
        self._repo = UserRepository()

    def execute(self, username: str)-> ResponseUserSchema:
        with self._db.session() as session:
            user = self._repo.get_user(session, username)

        return ResponseUserSchema.model_validate(obj=user)