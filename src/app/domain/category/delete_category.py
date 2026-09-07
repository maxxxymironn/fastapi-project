from app.core.exceptions.category_domain_exception import (
    CategoryNotDeletedException,
    CategoryNotFoundException,
    GeneralCategoryCannotBeModifiedException,
)
from app.core.exceptions.database_exception import (
    EntityNotDeletedException,
    EntityNotFoundException,
)
from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.category import CategoryRepository


class DeleteCategoryUseCase:
    def __init__(self):
        self._db = db
        self._repo = CategoryRepository()

    async def execute(self, category_slug: str) -> None:
        if category_slug == "general":
            raise GeneralCategoryCannotBeModifiedException()
        try:
            async with self._db.session() as session:
                await self._repo.delete(session, category_slug)
        except EntityNotFoundException:
            raise CategoryNotFoundException(category_slug=category_slug)
        except EntityNotDeletedException:
            raise CategoryNotDeletedException(category_slug=category_slug)
