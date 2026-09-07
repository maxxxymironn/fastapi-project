from app.core.exceptions.category_domain_exception import (
    CategoryAlreadyExistsException,
    CategoryNotFoundException,
    GeneralCategoryCannotBeModifiedException,
)
from app.core.exceptions.database_exception import (
    EntityAlreadyExistsException,
    EntityNotFoundException,
)
from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.category import CategoryRepository
from app.schemas.category import EditCategorySchema, ResponseCategorySchema


class EditCategoryUseCase:
    def __init__(self):
        self._db = db
        self._repo = CategoryRepository()

    async def execute(
        self, category_slug: str, category_data: EditCategorySchema
    ) -> ResponseCategorySchema:
        if category_slug == "general":
            raise GeneralCategoryCannotBeModifiedException()
        try:
            async with self._db.session() as session:
                category = await self._repo.edit(session, category_slug, category_data)
        except EntityNotFoundException:
            raise CategoryNotFoundException(category_slug=category_slug)
        except EntityAlreadyExistsException:
            raise CategoryAlreadyExistsException(category_slug=category_slug)

        return ResponseCategorySchema.model_validate(category)
