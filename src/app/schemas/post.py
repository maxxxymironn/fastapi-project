from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BasePostSchema(BaseModel):
    is_published: bool | None = True
    image_url: str | None = None


class EditPostSchema(BasePostSchema):
    title: str | None = Field(default=None, max_length=256)
    text: str | None = None


class CreatePostSchema(BasePostSchema):
    title: str = Field(max_length=128)
    text: str
    author_username: str
    publicated_at: datetime | None = None
    category_slug: str
    location_name: str | None = None


class ResponseAuthorSchema(BaseModel):
    id: int
    username: str
    email: str | None
    first_name: str | None
    last_name: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResponsePostSchemaWithourAuthor(CreatePostSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResponsePostSchema(ResponsePostSchemaWithourAuthor):
    author: ResponseAuthorSchema

    model_config = ConfigDict(from_attributes=True)
