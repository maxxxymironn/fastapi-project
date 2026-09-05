from app.domain.post.create_post import CreatePostUseCase
from app.domain.post.delete_post import DeletePostUseCase
from app.domain.post.edit_post import EditPostUseCase
from app.domain.post.get_post_by_title import GetPostByTitleUseCase
from app.domain.post.get_post_list import GetPostListUseCase


def get_create_post_case() -> CreatePostUseCase:
    return CreatePostUseCase()


def get_get_post_by_title_case() -> GetPostByTitleUseCase:
    return GetPostByTitleUseCase()


def get_delete_post_case() -> DeletePostUseCase:
    return DeletePostUseCase()


def get_edit_post_case() -> EditPostUseCase:
    return EditPostUseCase()


def get_get_post_list_case() -> GetPostListUseCase:
    return GetPostListUseCase()
