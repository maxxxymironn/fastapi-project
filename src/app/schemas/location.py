from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CreateLocationSchema(BaseModel):
    name: str = Field(max_length=256)
    is_published: bool = True


class ResponseLocationSchema(CreateLocationSchema):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
