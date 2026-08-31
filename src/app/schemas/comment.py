from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EditCommentSchema(BaseModel):
    text: str
    image_url: str | None


class CreateCommentSchema(EditCommentSchema):
    author_id: int


class ResponseCommentSchema(CreateCommentSchema):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)