from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator

from app.core.constants import EMAIL_REGEX
from app.schemas.post import ResponsePostSchemaWithourAuthor
from app.services.validate_attribute import validate_attribute


class BaseUserSchema(BaseModel):
    email: str | None = Field(
        default=None,
        max_length=128,
        pattern=EMAIL_REGEX,
        examples=["email@google.com | null"]
    )
    first_name: str | None = Field(
        default=None,
        max_length=128,
        examples=["first_name | null"]
    )
    last_name: str | None = Field(
        default=None,
        max_length=128,
        examples=["last_name | null"]
    )


class EditUserSchema(BaseUserSchema):
    username: str | None = Field(
        default=None,
        min_length=5,
        max_length=128,
        examples=["username | null"]
    )

    @field_validator("username", mode="after")
    @staticmethod
    def validate_username(username: str | None) -> str | None:
        if not username:
            return None

        validate_attribute("username", username)
        return username


class CreateUserSchema(BaseUserSchema):
    username: str = Field(min_length=5, max_length=128, examples=["username"])
    password: str = Field(min_length=8, max_length=128, examples=["password"])

    @field_validator("username", mode="after")
    @staticmethod
    def validate_username(username: str) -> str:
        validate_attribute("username", username)
        return username


class ResponseUserSchema(BaseUserSchema):
    id: int
    password: SecretStr = Field(max_length=128)
    username: str = Field(max_length=128)
    created_at: datetime
    posts: list[ResponsePostSchemaWithourAuthor]

    model_config = ConfigDict(from_attributes=True)
