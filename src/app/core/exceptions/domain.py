class BaseDomainException(Exception):
    def __init__(self, detail: str) -> None:
        self._detail = detail

    def get_detail(self) -> str:
        return self._detail


class UserNotFoundByUsernameException(BaseDomainException):
    _exception_text_template = "User with username='{username}' not found"

    def __init__(self, username: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            username=username
        )

        super().__init__(detail=self._exception_text_template)


class GetUserListException(BaseDomainException):
    def __init__(self) -> None:
        super().__init__(detail="Getting user list raises exception")


class UserIsNotUniqueException(BaseDomainException):
    _exception_text_templates = [
        "User with username='{username}' or email='{email}' already exists",
        "User with username='{username}' already exists",
        "User with email='{email} already exists'",
    ]

    def __init__(self, username: str | None, email: str | None) -> None:
        if not email:
            self._exception_text_template = self._exception_text_templates[1].format(
                username=username
            )
        elif not username:
            self._exception_text_template = self._exception_text_templates[2].format(
                email=email
            )
        else:
            self._exception_text_template = self._exception_text_templates[0].format(
                username=username, email=email
            )

        super().__init__(detail=self._exception_text_template)


class UserNotDeletedException(BaseDomainException):
    _exception_text_template = "User with username='{username}' can't be deleted"

    def __init__(self, username: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            username=username
        )

        super().__init__(detail=self._exception_text_template)
