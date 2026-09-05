from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, SecretStr

from app.schemas.post import ResponsePostSchemaWithourAuthor


class BaseUserSchema(BaseModel):
    email: str | None = Field(default=None, max_length=128)
    first_name: str | None = Field(default=None, max_length=128)
    last_name: str | None = Field(default=None, max_length=128)


class EditUserSchema(BaseUserSchema):
    username: str | None = Field(default=None, max_length=128)


class CreateUserSchema(BaseUserSchema):
    username: str = Field(max_length=128)
    password: str = Field(max_length=128)


class ResponseUserSchema(BaseUserSchema):
    id: int
    password: SecretStr = Field(max_length=128)
    username: str = Field(max_length=128)
    created_at: datetime
    posts: list[ResponsePostSchemaWithourAuthor]

    model_config = ConfigDict(from_attributes=True)
