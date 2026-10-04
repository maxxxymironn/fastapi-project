from app.core.exceptions.database_exception import EntityAlreadyExistsException
from app.core.exceptions.user_domain_exception import UserIsNotUniqueException
from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.user import UserRepository
from app.schemas.user import CreateUserSchema, ResponseUserSchema
from app.services.password import get_password_hash


class CreateUserUseCase:
    def __init__(self):
        self._db = db
        self._repo = UserRepository()

    async def execute(self, user_data: CreateUserSchema) -> ResponseUserSchema:
        try:
            user_data.password = get_password_hash(user_data.password)

            async with self._db.session() as session:
                user = await self._repo.create_user(session, user_data)
        except EntityAlreadyExistsException:
            raise UserIsNotUniqueException(
                username=user_data.username, email=user_data.email
            )

        return ResponseUserSchema.model_validate(user)
