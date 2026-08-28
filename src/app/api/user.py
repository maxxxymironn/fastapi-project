from fastapi import APIRouter, status, HTTPException, Depends

from app.schemas.user import CreateUserSchema, ResponseUserSchema
from app.domain.user.use_cases.get_user import GetUserByUsernameUseCase
from app.domain.user.use_cases.create_user import CreateUserUseCase
from app.api.depends import (
    get_case_get_user_by_username,
    get_case_create_user
)


router = APIRouter()


@router.get(
    "/profile/{username}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseUserSchema
)
def get_user_by_username(
    username: str,
    use_case: GetUserByUsernameUseCase = Depends(get_case_get_user_by_username)
) -> ResponseUserSchema:
    try:
        return use_case.execute(username)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post(
    "/profile",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseUserSchema
)
async def create_user(
    user_data: CreateUserSchema,
    use_case: CreateUserUseCase = Depends(get_case_create_user)
) -> ResponseUserSchema:
    try:
        return use_case.execute(user_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )


@router.patch(
    "/profile/{username}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseUserSchema
)
async def edit_profile(login: str, new_username: str):
    pass
