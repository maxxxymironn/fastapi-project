from datetime import datetime

from slugify import slugify
from sqlalchemy import DateTime, String, Text, event, func
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastucture.database import Base


class CategoryModel(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(256))
    slug: Mapped[str] = mapped_column(String, unique=True)
    description: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    is_published: Mapped[bool] = mapped_column(default=True)
