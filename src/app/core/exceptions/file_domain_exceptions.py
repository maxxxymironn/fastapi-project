from .base_domain_exception import BaseDomainException


class UploadFileIsNotImageException(BaseDomainException):
    def __init__(self) -> None:
        super().__init__(
            detail="Upload file has not supported extension: '.jpeg', '.jpg'"
        )


class TooManyUploadFilesException(BaseDomainException):
    def __init__(self) -> None:
        super().__init__(
            detail="Too many upload files. Maximum = 9"
        )


class UploadFileHasNotNameException(BaseDomainException):
    def __init__(self) -> None:
        super().__init__(detail="Upload file has not name")


class NoImageException(BaseDomainException):
    def __init__(self) -> None:
        super().__init__(detail="No image")
