from fastapi import APIRouter, Depends, HTTPException, status

from app.api.depends import (
    get_case_create_user,
    get_case_edit_user,
    get_case_get_user_by_username,
    get_delete_user_case,
)
from app.domain.user.use_cases.create_user import CreateUserUseCase
from app.domain.user.use_cases.delete_user import DeleteUserUseCase
from app.domain.user.use_cases.edit_user import EditUserUseCase
from app.domain.user.use_cases.get_user import GetUserByUsernameUseCase
from app.schemas.user import CreateUserSchema, EditUserSchema, ResponseUserSchema

router = APIRouter()


@router.get(
    "/profile/{username}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseUserSchema,
)
async def get_user_by_username(
    username: str,
    use_case: GetUserByUsernameUseCase = Depends(get_case_get_user_by_username),
) -> ResponseUserSchema:
    try:
        return await use_case.execute(username)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post(
    "/profile", status_code=status.HTTP_201_CREATED, response_model=ResponseUserSchema
)
async def create_user(
    user_data: CreateUserSchema,
    use_case: CreateUserUseCase = Depends(get_case_create_user),
) -> ResponseUserSchema:
    try:
        return await use_case.execute(user_data)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.patch(
    "/profile/{username}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseUserSchema,
)
async def edit_profile(
    username: str,
    user_data: EditUserSchema,
    use_case: EditUserUseCase = Depends(get_case_edit_user)
) -> ResponseUserSchema:
    try:
        return await use_case.execute(username, user_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.delete(
    "/profiles/{username}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(
    username: str,
    use_case: DeleteUserUseCase = Depends(get_delete_user_case)
) -> None:
    try:
        return await use_case.execute(username)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
