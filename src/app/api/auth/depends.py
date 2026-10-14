from app.domain.auth.authenticate_user import AuthenticateUserUseCase
from app.domain.auth.create_access_token import CreateAccessTokenUseCase
from app.domain.auth.create_tokens import CreateTokensUseCase
from app.domain.auth.refresh_tokens import RefreshTokensUseCase


def get_authenticate_user_case() -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase()


def get_create_acess_token_case() -> CreateAccessTokenUseCase:
    return CreateAccessTokenUseCase()


def get_create_tokens_case() -> CreateTokensUseCase:
    return CreateTokensUseCase()


def get_refresh_tokens_case() -> RefreshTokensUseCase:
    return RefreshTokensUseCase()