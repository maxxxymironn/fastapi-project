from app.infrastucture.database import db
from app.infrastucture.repositories.user import UserRepository


class DeleteUserUseCase:
    def __init__(self):
        self._db = db
        self._repo = UserRepository()

    async def execute(self, username: str) -> None:
        with self._db.session() as session:
            await self._repo.delete_user(session, username)
