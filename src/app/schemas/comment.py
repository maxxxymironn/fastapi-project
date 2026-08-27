from datetime import datetime

from pydantic import BaseModel


class CreateCommentSchema(BaseModel):
    text: str
    image_url: str | None
    post_id: int
    author_id: int


class ResponseCommentSchema(BaseModel):
    id: int
    text: str
    image_url: str | None
    post_id: int
    author_id: int
    created_at: datetime