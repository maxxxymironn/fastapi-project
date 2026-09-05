from datetime import datetime

from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator

from app.schemas.post import ResponsePostSchemaWithourAuthor


ALLOW_USERNAME_SYMBOLS = "qwertyuiopasdfghjklzxcvbnm0123456789_-"
EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"


def check_username(username: str) -> None:
    string = username.lower()
    for char in string:
        if ALLOW_USERNAME_SYMBOLS.find(char) == -1:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="username can only contains: a-z, 0-9, _, -",
            )


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
        max_length=128,
        examples=["username | null"]
    )

    @field_validator("username", mode="after")
    @staticmethod
    def check_first_name(username: str | None) -> str | None:
        if not username:
            return None

        check_username(username)
        return username


class CreateUserSchema(BaseUserSchema):
    username: str = Field(max_length=128, examples=["username"])
    password: str = Field(max_length=128, examples=["password"])

    @field_validator("username", mode="after")
    @staticmethod
    def check_first_name(username: str) -> str:
        check_username(username)
        return username


class ResponseUserSchema(BaseUserSchema):
    id: int
    password: SecretStr = Field(max_length=128)
    username: str = Field(max_length=128)
    created_at: datetime
    posts: list[ResponsePostSchemaWithourAuthor]

    model_config = ConfigDict(from_attributes=True)
