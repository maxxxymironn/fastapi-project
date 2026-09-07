from fastapi import APIRouter, Depends, HTTPException, status

from app.api.category.depends import (
    get_create_category_case,
    get_delete_category_case,
    get_edit_category_case,
    get_get_category_case,
    get_get_category_list_case,
)
from app.core.exceptions.category_domain_exception import (
    CategoryAlreadyExistsException,
    CategoryNotDeletedException,
    CategoryNotFoundException,
    GeneralCategoryCannotBeModifiedException,
    GetCategoryListException,
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
    except GetCategoryListException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exc.get_detail()
        )


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
    except CategoryNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )


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
    except CategoryAlreadyExistsException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail()
        )


@router.patch(
    "/category/{category_slug}",
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
    except CategoryNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    except GeneralCategoryCannotBeModifiedException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exc.get_detail()
        )


@router.delete(
    "/category/{category_slug}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_category(
    category_slug: str,
    use_case: DeleteCategoryUseCase = Depends(get_delete_category_case)
) -> None:
    try:
        await use_case.execute(category_slug)
    except CategoryNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    except CategoryNotDeletedException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail()
        )
    except GeneralCategoryCannotBeModifiedException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exc.get_detail()
        )
