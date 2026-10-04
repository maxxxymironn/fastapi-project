from app.domain.auth.authenticate_user import AuthenticateUserUseCase
from app.domain.auth.create_access_token import CreateAccessTokenUseCase


def get_authenticate_user_case() -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase()


def get_create_acess_token_case() -> CreateAccessTokenUseCase:
    return CreateAccessTokenUseCase()
