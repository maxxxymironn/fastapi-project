from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.auth.depends import get_authenticate_user_case, get_create_acess_token_case
from app.core.exceptions.user_domain_exception import (
    UserNotFoundByUsernameException,
)
from app.domain.auth.authenticate_user import AuthenticateUserUseCase
from app.domain.auth.create_access_token import CreateAccessTokenUseCase
from app.schemas.auth import TokenSchema

router = APIRouter()


@router.post("/token", response_model=TokenSchema)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_use_case: AuthenticateUserUseCase = Depends(get_authenticate_user_case),
    create_token_use_case: CreateAccessTokenUseCase = Depends(
        get_create_acess_token_case
    )
) -> TokenSchema:
    try:
        user = await auth_use_case.execute(form_data.username, form_data.password)
    except UserNotFoundByUsernameException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())

    access_token = await create_token_use_case.execute(login=user.username)

    return TokenSchema(access_token=access_token, token_type="bearer")
