from app.core.exceptions.database_exception import EntityListException
from app.core.exceptions.user_domain import GetUserListException
from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.user import UserRepository
from app.schemas.user import ResponseUserSchema


class GetUserListUseCase:
    def __init__(self):
        self._db = db
        self._repo = UserRepository()

    async def execute(self) -> list[ResponseUserSchema]:
        try:
            async with self._db.session() as session:
                user_list = await self._repo.get_user_list(session)
        except EntityListException:
            raise GetUserListException()

        return [
            ResponseUserSchema.model_validate(user) for user in user_list
        ]
