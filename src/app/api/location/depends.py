from app.domain.location.create_location import CreateLocationUseCase
from app.domain.location.delete_location import DeleteLocationUseCase
from app.domain.location.get_location import GetLocationUseCase
from app.domain.location.get_location_list import GetLocationListUseCase


def get_get_location_list_case() -> GetLocationListUseCase:
    return GetLocationListUseCase()


def get_get_location_case() -> GetLocationUseCase:
    return GetLocationUseCase()


def get_create_location_case() -> CreateLocationUseCase:
    return CreateLocationUseCase()


def get_delete_location_case() -> DeleteLocationUseCase:
    return DeleteLocationUseCase()
