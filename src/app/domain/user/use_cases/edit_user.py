from app.infrastucture.database import db
from app.infrastucture.repositories.user import UserRepository
from app.schemas.user import EditUserSchema, ResponseUserSchema


class EditUserUseCase:
    def __init__(self):
        self._db = db
        self._repo = UserRepository()

    async def execute(
        self, username: str, user_data: EditUserSchema
    ) -> ResponseUserSchema:
        with self._db.session() as session:
            user = await self._repo.update_user_attributes(session, username, user_data)

        return ResponseUserSchema.model_validate(obj=user)
