from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResponseCommentSchema(BaseModel):
    id: int
    text: str
    author_id: int
    created_at: datetime
    image_path: str | None

    model_config = ConfigDict(from_attributes=True)
