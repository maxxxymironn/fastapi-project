from app.core.exceptions.category_domain_exception import CategoryAlreadyExistsException
from app.core.exceptions.database_exception import EntityAlreadyExistsException
from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.category import CategoryRepository
from app.schemas.category import CreateCategorySchema, ResponseCategorySchema


class CreateCategoryUseCase:
    def __init__(self):
        self._db = db
        self._repo = CategoryRepository()

    async def execute(
        self, category_data: CreateCategorySchema
    ) -> ResponseCategorySchema:
        try:
            async with self._db.session() as session:
                category = await self._repo.create(session, category_data)
        except EntityAlreadyExistsException:
            # pyrefly: ignore [bad-argument-type]
            raise CategoryAlreadyExistsException(category_slug=category_data.slug)

        return ResponseCategorySchema.model_validate(category)
