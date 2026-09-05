from app.domain.category.create_category import CreateCategoryUseCase
from app.domain.category.delete_category import DeleteCategoryUseCase
from app.domain.category.edit_category import EditCategoryUseCase
from app.domain.category.get_category import GetCategoryUseCase
from app.domain.category.get_category_list import GetCategoryListUseCase


def get_create_category_case() -> CreateCategoryUseCase:
    return CreateCategoryUseCase()


def get_get_category_list_case() -> GetCategoryListUseCase:
    return GetCategoryListUseCase()


def get_get_category_case() -> GetCategoryUseCase:
    return GetCategoryUseCase()


def get_edit_category_case() -> EditCategoryUseCase:
    return EditCategoryUseCase()


def get_delete_category_case() -> DeleteCategoryUseCase:
    return DeleteCategoryUseCase()
