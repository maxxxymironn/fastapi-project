from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EditCategorySchema(BaseModel):
    description: str | None = None
    is_published: bool | None = None


class CreateCategorySchema(BaseModel):
    title: str = Field(max_length=256)
    description: str
    slug: str | None = Field(default=None, max_length=256)
    is_published: bool = True


class ResponseCategorySchema(CreateCategorySchema):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
