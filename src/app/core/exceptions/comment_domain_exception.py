class BaseDomainException(Exception):
    def __init__(self, detail: str) -> None:
        self._detail = detail

    def get_detail(self) -> str:
        return self._detail


class CommentNotFoundException(BaseDomainException):
    _exception_text_template = "Comment with id='{id}' not found"

    def __init__(self, comment_id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(
            id=comment_id
        )

        super().__init__(detail=self._exception_text_template)


class GetCommentListException(BaseDomainException):
    def __init__(self) -> None:
        super().__init__(detail="Getting comments raised exception")


class CommentNotCreatedException(BaseDomainException):
    def __init__(self) -> None:
        super().__init__(detail="Comment not created")


class CommentNotDeletedException(BaseDomainException):
    _exception_text_template = "Comment with id='{id}' cannot be deleted"

    def __init__(self, comment_id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(
            id=comment_id
        )

        super().__init__(detail=self._exception_text_template)
