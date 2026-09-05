from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.user import UserRepository
from app.schemas.user import ResponseUserSchema


class GetUserByUsernameUseCase:
    def __init__(self):
        self._db = db
        self._repo = UserRepository()

    async def execute(self, username: str) -> ResponseUserSchema:
        async with self._db.session() as session:
            user = await self._repo.get_user(session, username)

        return ResponseUserSchema.model_validate(obj=user)
