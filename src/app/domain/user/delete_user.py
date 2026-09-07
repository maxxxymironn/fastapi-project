from app.core.exceptions.database_exception import (
    EntityNotDeletedException,
    EntityNotFoundException,
)
from app.core.exceptions.user_domain_exception import (
    UserNotDeletedException,
    UserNotFoundByUsernameException,
)
from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.user import UserRepository


class DeleteUserUseCase:
    def __init__(self):
        self._db = db
        self._repo = UserRepository()

    async def execute(self, username: str) -> None:
        try:
            async with self._db.session() as session:
                await self._repo.delete_user(session, username)
        except EntityNotFoundException:
            raise UserNotFoundByUsernameException(username)
        except EntityNotDeletedException:
            raise UserNotDeletedException(username)
