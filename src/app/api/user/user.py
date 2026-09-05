from fastapi import APIRouter, Depends, HTTPException, status

from app.api.user.depends import (
    get_create_user_case,
    get_delete_user_case,
    get_edit_user_case,
    get_get_user_by_username_case,
    get_get_user_list_case,
)
from app.core.exceptions.domain import (
    GetUserListException,
    UserIsNotUniqueException,
    UserNotDeletedException,
    UserNotFoundByUsernameException,
)
from app.domain.user.create_user import CreateUserUseCase
from app.domain.user.delete_user import DeleteUserUseCase
from app.domain.user.edit_user import EditUserUseCase
from app.domain.user.get_user import GetUserByUsernameUseCase
from app.domain.user.get_user_list import GetUserListUseCase
from app.schemas.user import CreateUserSchema, EditUserSchema, ResponseUserSchema

router = APIRouter()


@router.get(
    "/profile/{username}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseUserSchema,
)
async def get_user_by_username(
    username: str,
    use_case: GetUserByUsernameUseCase = Depends(get_get_user_by_username_case),
) -> ResponseUserSchema:
    try:
        return await use_case.execute(username)
    except UserNotFoundByUsernameException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )


@router.get(
    "/users", status_code=status.HTTP_200_OK, response_model=list[ResponseUserSchema]
)
async def get_user_list(
    use_case: GetUserListUseCase = Depends(get_get_user_list_case),
) -> list[ResponseUserSchema]:
    try:
        return await use_case.execute()
    except GetUserListException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc)


@router.post(
    "/profile", status_code=status.HTTP_201_CREATED, response_model=ResponseUserSchema
)
async def create_user(
    user_data: CreateUserSchema,
    use_case: CreateUserUseCase = Depends(get_create_user_case),
) -> ResponseUserSchema:
    try:
        return await use_case.execute(user_data)
    except UserIsNotUniqueException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail()
        )


@router.patch(
    "/profile/{username}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseUserSchema,
)
async def edit_profile(
    username: str,
    user_data: EditUserSchema,
    use_case: EditUserUseCase = Depends(get_edit_user_case),
) -> ResponseUserSchema:
    try:
        return await use_case.execute(username, user_data)
    except UserNotFoundByUsernameException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    except UserIsNotUniqueException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail()
        )


@router.delete("/profiles/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    username: str, use_case: DeleteUserUseCase = Depends(get_delete_user_case)
) -> None:
    try:
        return await use_case.execute(username)
    except UserNotFoundByUsernameException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    except UserNotDeletedException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail()
        )
