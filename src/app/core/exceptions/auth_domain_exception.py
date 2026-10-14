from app.core.exceptions.base_domain_exception import BaseDomainException


class TokenNotCreatedException(BaseDomainException):
    def __init__(self) -> None:
        super().__init__(detail="Token not created")