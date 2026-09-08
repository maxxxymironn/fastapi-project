from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.comment import ResponseCommentSchema


class BasePostSchema(BaseModel):
    is_published: bool | None = True
    image_url: str | None = None


class EditPostSchema(BasePostSchema):
    title: str | None = Field(default=None, max_length=256)
    text: str | None = None
    category_slug: str | None = None
    location_name: str | None = Field(
        default=None, max_length=256, examples=["string 256 | null"]
    )

    @field_validator("location_name", mode="after")
    @staticmethod
    def validate_location_name(location_name: str) -> str:
        return location_name.lower()


class CreatePostSchema(BasePostSchema):
    title: str = Field(min_length=5, max_length=128, examples=["title"])
    text: str = Field(examples=["some text"])
    publicated_at: datetime | None = None
    category_slug: str
    location_name: str | None = Field(
        default=None, max_length=256, examples=["string 256 | null"]
    )

    @field_validator("location_name", mode="after")
    @staticmethod
    def validate_location_name(location_name: str | None) -> str | None:
        if not location_name:
            return None
        return location_name.lower()


class ResponseAuthorSchema(BaseModel):
    id: int
    username: str
    email: str | None
    first_name: str | None
    last_name: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResponsePostSchemaWithourAuthorAndComments(CreatePostSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResponsePostSchema(ResponsePostSchemaWithourAuthorAndComments):
    author: ResponseAuthorSchema
    comments: list[ResponseCommentSchema]

    model_config = ConfigDict(from_attributes=True)
