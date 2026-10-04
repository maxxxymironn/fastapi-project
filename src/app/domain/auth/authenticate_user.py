from app.core.exceptions.database_exception import EntityNotFoundException
from app.core.exceptions.user_domain_exception import (
    UserNotFoundByUsernameException,
)
from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.user import UserRepository
from app.schemas.user import ResponseUserSchema


class AuthenticateUserUseCase:
    def __init__(self) -> None:
        self._db = db
        self._repo = UserRepository()

    async def execute(self, login: str, password: str) -> ResponseUserSchema:
        try:
            async with self._db.session() as session:
                user = await self._repo.get_user(session, username=login)
        except EntityNotFoundException:
            raise UserNotFoundByUsernameException(username=login)

        # verify password

        return ResponseUserSchema.model_validate(user)
