from app.core.exceptions.database import EntityNotFoundException
from app.core.exceptions.domain import UserNotFoundByUsernameException
from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.user import UserRepository
from app.schemas.user import ResponseUserSchema


class GetUserByUsernameUseCase:
    def __init__(self):
        self._db = db
        self._repo = UserRepository()

    async def execute(self, username: str) -> ResponseUserSchema:
        try:
            async with self._db.session() as session:
                user = await self._repo.get_user(session, username)
        except EntityNotFoundException:
            raise UserNotFoundByUsernameException(username)

        return ResponseUserSchema.model_validate(user)
