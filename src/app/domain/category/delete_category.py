from app.infrastucture.database import db
from app.infrastucture.repositories.category import CategoryRepository


class DeleteCategoryUseCase:
    def __init__(self):
        self._db = db
        self._repo = CategoryRepository()

    async def execute(self, category_slug: str) -> None:
        with self._db.session() as session:
            await self._repo.delete(session, category_slug)
