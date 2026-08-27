from datetime import datetime

from pydantic import BaseModel, Field


class PostCreateSchema(BaseModel):
    title: str = Field(max_length=128)
    text: str
    is_published: bool | None = None
    image_path: str | None = None
    author_id: int
    category_id: int | None = None
    location_id: int | None = None
    publicated_at: datetime | None = None


class PostResponseSchema(BaseModel):
    id: int
    title: str = Field(max_length=128)
    text: str
    is_published: bool
    image_path: str | None = None
    author_id: int
    category_id: int | None = None
    location_id: int | None = None
    publicated_at: datetime
    updated_at: datetime
