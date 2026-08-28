from datetime import datetime
from pydantic import BaseModel, SecretStr, Field, ConfigDict


class BaseUserSchema(BaseModel):
    username: str = Field(max_length=128)
    email: str | None = Field(default=None, max_length=128)
    first_name: str | None = Field(default=None, max_length=128)
    last_name: str | None = Field(default=None, max_length=128)


class CreateUserSchema(BaseUserSchema):
    password: str = Field(max_length=128)


class ResponseUserSchema(BaseUserSchema):
    id: int
    username: str = Field(max_length=128)
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
