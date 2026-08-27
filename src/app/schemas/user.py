from pydantic import BaseModel, SecretStr, Field


class CreateUserSchema(BaseModel):
    login: str = Field(max_length=128)
    password: SecretStr = Field(max_length=128)
    username: str | None = Field(login, max_length=128)


class ResponceUserSchema(BaseModel):
    id: int
    login: str = Field(max_length=128)
    password: SecretStr = Field(max_length=128)
    username: str