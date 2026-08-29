from app.infrastucture.database import db
from app.infrastucture.repositories.user import UserRepository
from app.schemas.user import CreateUserSchema, ResponseUserSchema


class CreateUserUseCase:
    def __init__(self):
        self._db = db
        self._repo = UserRepository()

    async def execute(self, user_data: CreateUserSchema) -> ResponseUserSchema:
        with self._db.session() as session:
            user = await self._repo.create_user(session, user_data)
            
        return ResponseUserSchema.model_validate(user)
        
