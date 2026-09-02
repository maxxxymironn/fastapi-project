from fastapi import APIRouter, Depends, HTTPException, status

from app.api.depends import (
    get_create_location_case,
    get_delete_location_case,
    get_get_location_case,
    get_get_location_list_case,
)
from app.domain.location.create_location import CreateLocationUseCase
from app.domain.location.delete_location import DeleteLocationUseCase
from app.domain.location.get_location import GetLocationUseCase
from app.domain.location.get_location_list import GetLocationListUseCase
from app.schemas.location import CreateLocationSchema, ResponseLocationSchema

router = APIRouter()


@router.get(
    "/locations",
    status_code=status.HTTP_200_OK,
    response_model=list[ResponseLocationSchema],
)
async def get_location_list(
    use_case: GetLocationListUseCase = Depends(get_get_location_list_case),
) -> list[ResponseLocationSchema]:
    try:
        return await use_case.execute()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get(
    "/locations/{location_name}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseLocationSchema,
)
async def get_location(
    location_name: str, use_case: GetLocationUseCase = Depends(get_get_location_case)
) -> ResponseLocationSchema:
    try:
        return await use_case.execute(location_name)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post(
    "/locations",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseLocationSchema,
)
async def create_location(
    location_data: CreateLocationSchema,
    use_case: CreateLocationUseCase = Depends(get_create_location_case),
) -> ResponseLocationSchema:
    try:
        return await use_case.execute(location_data)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.delete("/locations/{location_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    location_name: str,
    use_case: DeleteLocationUseCase = Depends(get_delete_location_case),
) -> None:
    try:
        await use_case.execute(location_name)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
