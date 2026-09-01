from fastapi import APIRouter, Depends, HTTPException, status

from app.api.depends import (
    get_create_category_case,
    get_delete_category_case,
    get_edit_category_case,
    get_get_category_case,
    get_get_category_list_case,
)
from app.domain.category.create_category import CreateCategoryUseCase
from app.domain.category.delete_category import DeleteCategoryUseCase
from app.domain.category.edit_category import EditCategoryUseCase
from app.domain.category.get_category import GetCategoryUseCase
from app.domain.category.get_category_list import GetCategoryListUseCase
from app.schemas.category import (
    CreateCategorySchema,
    EditCategorySchema,
    ResponseCategorySchema,
)

router = APIRouter()


@router.get(
    "/category",
    status_code=status.HTTP_200_OK,
    response_model=list[ResponseCategorySchema]
)
async def get_category_list(
    use_case: GetCategoryListUseCase = Depends(get_get_category_list_case)
) -> list[ResponseCategorySchema]:
    try:
        return await use_case.execute()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get(
    "/category/{category_slug}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseCategorySchema
)
async def get_category(
    category_slug: str,
    use_case: GetCategoryUseCase = Depends(get_get_category_case)
) -> ResponseCategorySchema:
    try:
        return await use_case.execute(category_slug)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post(
    "/category",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseCategorySchema
)
async def create_category(
    category_data: CreateCategorySchema,
    use_case: CreateCategoryUseCase = Depends(get_create_category_case)
) -> ResponseCategorySchema:
    try:
        return await use_case.execute(category_data)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.patch(
    "/category",
    status_code=status.HTTP_200_OK,
    response_model=ResponseCategorySchema
)
async def edit_category(
    category_slug: str,
    category_data: EditCategorySchema,
    use_case: EditCategoryUseCase = Depends(get_edit_category_case)
) -> ResponseCategorySchema:
    try:
        return await use_case.execute(category_slug, category_data)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.delete(
    "/category",
    status_code=status.HTTP_200_OK,
    response_model=ResponseCategorySchema
)
async def delete_category(
    category_slug: str,
    use_case: DeleteCategoryUseCase = Depends(get_delete_category_case)
) -> None:
    try:
        await use_case.execute(category_slug)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
