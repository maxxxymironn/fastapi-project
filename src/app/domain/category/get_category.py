from app.core.exceptions.category_domain_exception import CategoryNotFoundException
from app.core.exceptions.database_exception import EntityNotFoundException
from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.category import CategoryRepository
from app.schemas.category import ResponseCategorySchema


class GetCategoryUseCase:
    def __init__(self):
        self._db = db
        self._repo = CategoryRepository()

    async def execute(self, category_slug: str) -> ResponseCategorySchema:
        try:
            async with self._db.session() as session:
                category = await self._repo.get(session, category_slug)
        except EntityNotFoundException:
            raise CategoryNotFoundException(category_slug=category_slug)

        return ResponseCategorySchema.model_validate(category)
