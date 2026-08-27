from fastapi import APIRouter, status

from app.schemas.user import CreateUserSchema, ResponceUserSchema


router = APIRouter()


@router.get(
    "/profile/{username}",
    status_code=status.HTTP_200_OK,
    response_model=ResponceUserSchema
)
async def get_profile(username: str):
    pass


@router.patch(
    "/profile/{username}",
    status_code=status.HTTP_200_OK,
    response_model=ResponceUserSchema
)
async def edit_profile(username: str, new_username: str):
    pass
