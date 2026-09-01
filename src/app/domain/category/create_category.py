from slugify import slugify

from app.infrastucture.database import db
from app.infrastucture.repositories.category import CategoryRepository
from app.schemas.category import CreateCategorySchema, ResponseCategorySchema


class CreateCategoryUseCase:
    def __init__(self):
        self._db = db
        self._repo = CategoryRepository()

    async def execute(
        self, category_data: CreateCategorySchema
    ) -> ResponseCategorySchema:
        if not category_data.slug:
            category_data.slug = slugify(
                category_data.title, lowercase=True, max_length=256
            )

        with self._db.session() as session:
            category = await self._repo.create(session, category_data)

        return ResponseCategorySchema.model_validate(category)
