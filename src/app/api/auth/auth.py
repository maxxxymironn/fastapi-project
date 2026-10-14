from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.auth.depends import (
    get_authenticate_user_case,
    get_create_tokens_case,
    get_refresh_tokens_case,
)
from app.core.exceptions.auth_domain_exception import TokenNotCreatedException
from app.core.exceptions.auth_exception import WrongPasswordException
from app.core.exceptions.user_domain_exception import UserNotFoundByUsernameException
from app.domain.auth.authenticate_user import AuthenticateUserUseCase
from app.domain.auth.create_tokens import CreateTokensUseCase
from app.domain.auth.refresh_tokens import RefreshTokensUseCase
from app.schemas.auth import RefreshTokenSchema, TokenSchema

router = APIRouter()


@router.post("/token", response_model=TokenSchema)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_use_case: Annotated[
        AuthenticateUserUseCase, Depends(get_authenticate_user_case)
    ],
    create_tokens_use_case: CreateTokensUseCase = Depends(
        get_create_tokens_case
    )
) -> TokenSchema:
    try:
        user = await auth_use_case.execute(form_data.username, form_data.password)
    except UserNotFoundByUsernameException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    except WrongPasswordException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exc.get_detail()
        )

    try:
        access_token, refresh_token = await (
            create_tokens_use_case.execute(login=user.username)
        )
    except TokenNotCreatedException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exc.get_detail()
        )

    return TokenSchema(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/refresh", response_model=TokenSchema)
async def refresh_tokens(
    input_refresh_token: RefreshTokenSchema,
    refresh_tokens_use_case: RefreshTokensUseCase = Depends(get_refresh_tokens_case)
) -> TokenSchema:
    try:
        access_token, refresh_token = await (
            refresh_tokens_use_case.execute(input_refresh_token)
        )
    except TokenNotCreatedException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exc.get_detail()
        )

    return TokenSchema(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )
