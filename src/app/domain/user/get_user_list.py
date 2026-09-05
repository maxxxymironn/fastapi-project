from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.user import UserRepository
from app.schemas.user import ResponseUserSchema


class GetUserListUseCase:
    def __init__(self):
        self._db = db
        self._repo = UserRepository()

    async def execute(self) -> list[ResponseUserSchema]:
        async with self._db.session() as session:
            user_list = await self._repo.get_user_list(session)

        return [
            ResponseUserSchema.model_validate(user) for user in user_list
        ]
