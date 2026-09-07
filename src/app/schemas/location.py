from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.services.validate_attribute import validate_attribute


class CreateLocationSchema(BaseModel):
    name: str = Field(max_length=256, examples=["string 256"])
    is_published: bool = Field(default=True, examples=[True, False])

    @field_validator("name", mode="after")
    @staticmethod
    def validate_name(name: str) -> str:
        validate_attribute("location", name)
        return name.lower()


class ResponseLocationSchema(CreateLocationSchema):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
