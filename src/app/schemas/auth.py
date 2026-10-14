from pydantic import BaseModel, Field


class RefreshTokenSchema(BaseModel):
    refresh_token: str = Field(description="Токен для продления доступа к системе")


class TokenSchema(RefreshTokenSchema):
    access_token: str = Field(description="Токен для доступа к системе")
    token_type: str = Field(description="Тип токена для доступа к системе")
