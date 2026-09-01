from app.infrastucture.database import db
from app.infrastucture.repositories.category import CategoryRepository
from app.schemas.category import EditCategorySchema, ResponseCategorySchema


class EditCategoryUseCase:
    def __init__(self):
        self._db = db
        self._repo = CategoryRepository()

    async def execute(
        self, category_slug: str, category_data: EditCategorySchema
    ) -> ResponseCategorySchema:
        with self._db.session() as session:
            category = await self._repo.edit(session, category_slug, category_data)

        return ResponseCategorySchema.model_validate(category)
