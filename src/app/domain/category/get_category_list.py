from app.core.exceptions.category_domain_exception import GetCategoryListException
from app.core.exceptions.database_exception import EntityListException
from app.infrastucture.postgresql.database import db
from app.infrastucture.repositories.category import CategoryRepository
from app.schemas.category import ResponseCategorySchema


class GetCategoryListUseCase:
    def __init__(self):
        self._db = db
        self._repo = CategoryRepository()

    async def execute(self) -> list[ResponseCategorySchema]:
        try:
            async with self._db.session() as session:
                category_list = await self._repo.get_list(session)
        except EntityListException:
            raise GetCategoryListException()

        return [
            ResponseCategorySchema.model_validate(category)
            for category in category_list
        ]
