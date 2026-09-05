from app.core.exceptions.database import (
    EntityAlreadyExistsException,
    EntityNotFoundException,
)
from app.core.exceptions.domain import (
    UserIsNotUniqueException,
    UserNotFoundByUsernameException,
)
from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.user import UserRepository
from app.schemas.user import EditUserSchema, ResponseUserSchema


class EditUserUseCase:
    def __init__(self):
        self._db = db
        self._repo = UserRepository()

    async def execute(
        self, username: str, user_data: EditUserSchema
    ) -> ResponseUserSchema:
        try:
            async with self._db.session() as session:
                user = await self._repo.update_user_attributes(
                    session, username, user_data
                )
        except EntityNotFoundException:
            raise UserNotFoundByUsernameException(username)
        except EntityAlreadyExistsException:
            raise UserIsNotUniqueException(
                username=user_data.username, email=user_data.email
            )

        return ResponseUserSchema.model_validate(user)
