from .base_domain_exception import BaseDomainException


class LocationNotFoundException(BaseDomainException):
    _exception_text_template = "Location with name='{name}' not found"

    def __init__(self, location_name: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            name=location_name
        )

        super().__init__(detail=self._exception_text_template)


class GetLocationListException(BaseDomainException):
    def __init__(self) -> None:
        super().__init__(detail="Getting Location list raised exception")


class LocationAlreadyExistsException(BaseDomainException):
    _exception_text_template = "Location with name='{name}' already exists"

    def __init__(self, location_name: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            name=location_name
        )

        super().__init__(detail=self._exception_text_template)


class LocationNotDeletedException(BaseDomainException):
    _exception_text_template = "Location with name='{name}' cannot be deleted"

    def __init__(self, location_name: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            name=location_name
        )

        super().__init__(detail=self._exception_text_template)
