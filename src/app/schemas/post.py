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


class ResponsePostSchema(CreatePostSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
