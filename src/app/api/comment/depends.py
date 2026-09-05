from app.domain.comment.create_comment import CreateCommentUseCase
from app.domain.comment.delete_comment import DeleteCommentUseCase
from app.domain.comment.edit_comment import EditCommentUseCase
from app.domain.comment.get_comment_list import GetCommentListUseCase


def get_get_comment_list_case() -> GetCommentListUseCase:
    return GetCommentListUseCase()


def get_create_comment_case() -> CreateCommentUseCase:
    return CreateCommentUseCase()


def get_edit_comment_case() -> EditCommentUseCase:
    return EditCommentUseCase()


def get_delete_comment_case() -> DeleteCommentUseCase:
    return DeleteCommentUseCase()
