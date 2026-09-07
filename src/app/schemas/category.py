from datetime import datetime

from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic_core.core_schema import ValidationInfo
from slugify import slugify

from app.services.validate_attribute import validate_attribute


class EditCategorySchema(BaseModel):
    description: str | None = Field(default=None, examples=["string | null"])
    is_published: bool | None = Field(default=None, examples=[True, False])


class CreateCategorySchema(BaseModel):
    title: str = Field(max_length=256, examples=["string 256"])
    description: str
    slug: str | None = Field(default=None, max_length=256, examples=["string | null"])
    is_published: bool = True

    @field_validator("slug", mode="after")
    @staticmethod
    def validate_slug(slug: str | None, info: ValidationInfo) -> str:
        if not slug:
            try:
                slug = slugify(
                    info.data["title"], lowercase=True, max_length=256
                )
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail=f"Slug title='{info.data["title"]}' failed"
                )

        validate_attribute("slug", slug)
        return slug

    model_config = ConfigDict(validate_default=True)


class ResponseCategorySchema(CreateCategorySchema):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
