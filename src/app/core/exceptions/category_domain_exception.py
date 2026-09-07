class BaseDomainException(Exception):
    def __init__(self, detail: str) -> None:
        self._detail = detail

    def get_detail(self) -> str:
        return self._detail


class CategoryNotFoundException(BaseDomainException):
    _exception_text_template = "Category with slug='{slug}' not found"

    def __init__(self, category_slug: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            slug=category_slug
        )

        super().__init__(detail=self._exception_text_template)


class GetCategoryListException(BaseDomainException):
    def __init__(self) -> None:
        super().__init__(detail="Getting category list raises exception")


class CategoryAlreadyExistsException(BaseDomainException):
    _exception_text_template = "Category with slug='{slug}' already exists"

    def __init__(
        self, category_slug: str
    ) -> None:
        self._exception_text_template = self._exception_text_template.format(
            slug=category_slug,
        )

        super().__init__(detail=self._exception_text_template)


class CategoryNotDeletedException(BaseDomainException):
    _exception_text_template = "Category with slug='{slug}' can't be deleted"

    def __init__(self, category_slug: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            slug=category_slug
        )

        super().__init__(detail=self._exception_text_template)


class GeneralCategoryCannotBeModifiedException(BaseDomainException):
    def __init__(self) -> None:
        super().__init__(detail="Category with slug='general' cannot be modified")
