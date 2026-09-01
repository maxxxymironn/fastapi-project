from app.domain.category.create_category import CreateCategoryUseCase
from app.domain.category.delete_category import DeleteCategoryUseCase
from app.domain.category.edit_category import EditCategoryUseCase
from app.domain.category.get_category import GetCategoryUseCase
from app.domain.category.get_category_list import GetCategoryListUseCase
from app.domain.comment.create_comment import CreateCommentUseCase
from app.domain.comment.delete_comment import DeleteCommentUseCase
from app.domain.comment.edit_comment import EditCommentUseCase
from app.domain.comment.get_comment_list import GetCommentListUseCase
from app.domain.post.use_cases.create_post import CreatePostUseCase
from app.domain.post.use_cases.delete_post import DeletePostUseCase
from app.domain.post.use_cases.edit_post import EditPostUseCase
from app.domain.post.use_cases.get_post_by_title import GetPostByTitleUseCase
from app.domain.post.use_cases.get_post_list import GetPostListUseCase
from app.domain.user.use_cases.create_user import CreateUserUseCase
from app.domain.user.use_cases.edit_user import EditUserUseCase
from app.domain.user.use_cases.get_user import GetUserByUsernameUseCase


def get_case_create_user() -> CreateUserUseCase:
    return CreateUserUseCase()


def get_case_get_user_by_username() -> GetUserByUsernameUseCase:
    return GetUserByUsernameUseCase()


def get_case_edit_user() -> EditUserUseCase:
    return EditUserUseCase()


def get_case_create_post() -> CreatePostUseCase:
    return CreatePostUseCase()


def get_case_get_post_by_title() -> GetPostByTitleUseCase:
    return GetPostByTitleUseCase()


def get_case_delete_post() -> DeletePostUseCase:
    return DeletePostUseCase()


def get_case_edit_post() -> EditPostUseCase:
    return EditPostUseCase()


def get_case_get_post_list() -> GetPostListUseCase:
    return GetPostListUseCase()


def get_case_get_comment_list() -> GetCommentListUseCase:
    return GetCommentListUseCase()


def get_case_create_comment() -> CreateCommentUseCase:
    return CreateCommentUseCase()


def get_case_edit_comment() -> EditCommentUseCase:
    return EditCommentUseCase()


def get_case_delete_comment() -> DeleteCommentUseCase:
    return DeleteCommentUseCase()


def get_create_category_case() -> CreateCategoryUseCase:
    return CreateCategoryUseCase()


def get_get_category_list_case() -> GetCategoryListUseCase:
    return GetCategoryListUseCase()


def get_get_category_case() -> GetCategoryUseCase:
    return GetCategoryUseCase()


def get_edit_category_case() -> EditCategoryUseCase:
    return EditCategoryUseCase()


def get_delete_category_case() -> DeleteCategoryUseCase:
    return DeleteCategoryUseCase()
