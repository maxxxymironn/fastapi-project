from pydantic import BaseModel, Field


class TokenSchema(BaseModel):
    access_token: str = Field(description="Токен для доступа к системе")
    token_type: str = Field(description="Тип токена для доступа к системе")
