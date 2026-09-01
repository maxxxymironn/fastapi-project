from fastapi import HTTPException, status
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session

from app.infrastucture.models.category import CategoryModel
from app.schemas.category import CreateCategorySchema, EditCategorySchema


class CategoryRepository:
    def __init__(self):
        self._model = CategoryModel

    async def get(self, session: Session, category_slug: str) -> CategoryModel:
        query = select(self._model).where(self._model.slug == category_slug)

        category: CategoryModel | None = session.scalar(query)

        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return category

    async def get_list(self, session: Session):
        query = select(self._model)
        return session.scalars(query).all()

    async def create(
        self, session: Session, category_data: CreateCategorySchema
    ) -> CategoryModel:
        query = (
            insert(self._model)
            .values(category_data.model_dump())
            .returning(self._model)
        )

        try:
            category: CategoryModel | None = session.scalar(query)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        return category

    async def edit(
        self, session: Session, category_slug: str, category_data: EditCategorySchema
    ) -> CategoryModel:
        query = (
            update(self._model)
            .where(self._model.slug == category_slug)
            .values(category_data.model_dump(exclude_none=True, exclude_unset=True))
            .returning(self._model)
        )

        try:
            category = session.scalar(query)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        return category

    async def delete(self, session: Session, category_slug: str) -> None:
        query = (
            delete(self._model)
            .where(self._model.slug == category_slug)
            .returning(self._model)
        )

        try:
            is_deleted = session.scalar(query) is not None
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        if not is_deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
