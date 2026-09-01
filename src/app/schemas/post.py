from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class EditPostSchema(BaseModel):
    title: str = Field(max_length=256)
    text: str
    is_published: bool | None = True
    image_url: str | None = None


class CreatePostSchema(EditPostSchema):
    author_username: str
    publicated_at: datetime | None = None
    category_slug: str
    location_name: str | None = None


class ResponsePostSchema(CreatePostSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

