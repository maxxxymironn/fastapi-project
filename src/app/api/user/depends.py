from app.domain.user.create_user import CreateUserUseCase
from app.domain.user.delete_user import DeleteUserUseCase
from app.domain.user.edit_user import EditUserUseCase
from app.domain.user.get_user import GetUserByUsernameUseCase
from app.domain.user.get_user_list import GetUserListUseCase


def get_create_user_case() -> CreateUserUseCase:
    return CreateUserUseCase()


def get_get_user_list_case() -> GetUserListUseCase:
    return GetUserListUseCase()


def get_get_user_by_username_case() -> GetUserByUsernameUseCase:
    return GetUserByUsernameUseCase()


def get_edit_user_case() -> EditUserUseCase:
    return EditUserUseCase()


def get_delete_user_case() -> DeleteUserUseCase:
    return DeleteUserUseCase()
