class BaseDatabaseException(Exception):
    def __init__(self, detail: str | None = None) -> None:
        self._detail = detail


class EntityNotFoundException(BaseDatabaseException):
    pass


class EntityListException(BaseDatabaseException):
    pass


class EntityAlreadyExistsException(BaseDatabaseException):
    pass


class EntityNotDeletedException(BaseDatabaseException):
    pass


class EntityNotCreatedException(BaseDatabaseException):
    pass
