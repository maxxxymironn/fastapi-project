from app.domain.user.use_cases.create_user import CreateUserUseCase
from app.domain.user.use_cases.get_user import GetUserByUsernameUseCase
from app.domain.user.use_cases.update_user_attributes import UpdateUserAttributesUseCase


def get_case_create_user() -> CreateUserUseCase:
    return CreateUserUseCase()


def get_case_get_user_by_username() -> GetUserByUsernameUseCase:
    return GetUserByUsernameUseCase()


def get_case_update_user_attributes() -> UpdateUserAttributesUseCase:
    return UpdateUserAttributesUseCase()