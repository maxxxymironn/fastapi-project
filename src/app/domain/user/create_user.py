from app.core.exceptions.database import EntityAlreadyExistsException
from app.core.exceptions.domain import UserIsNotUniqueException
from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.user import UserRepository
from app.schemas.user import CreateUserSchema, ResponseUserSchema


class CreateUserUseCase:
    def __init__(self):
        self._db = db
        self._repo = UserRepository()

    async def execute(self, user_data: CreateUserSchema) -> ResponseUserSchema:
        try:
            async with self._db.session() as session:
                user = await self._repo.create_user(session, user_data)
        except EntityAlreadyExistsException:
            raise UserIsNotUniqueException(
                username=user_data.username, email=user_data.email
            )

        return ResponseUserSchema.model_validate(user)
