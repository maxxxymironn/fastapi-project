from .base_domain_exception import BaseDomainException


class PostNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Post with id='{id}' not found"

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(
            id=id
        )

        super().__init__(detail=self._exception_text_template)


class GetPostListException(BaseDomainException):
    def __init__(self) -> None:
        super().__init__(detail="Getting post list raises exception")


class PostNotCreatedException(BaseDomainException):
    _exception_text_templates = [
        "Category='{category}' or location='{location}' not exists",
        "Category='{category}' not exists",
        "Location='{location}' not exists"
    ]

    def __init__(
        self, category_slug: str | None, location_name: str | None
    ) -> None:
        if not location_name:
            self._exception_text_template = self._exception_text_templates[1].format(
                category=category_slug
            )
        elif not category_slug:
            self._exception_text_template = self._exception_text_templates[2].format(
                location=location_name
            )
        else:
            self._exception_text_template = self._exception_text_templates[0].format(
                category=category_slug, location=location_name
            )

        super().__init__(detail=self._exception_text_template)


class PostNotDeletedException(BaseDomainException):
    _exception_text_template = "Post with id='{id}' can't be deleted"

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(
            id=id
        )

        super().__init__(detail=self._exception_text_template)
