from datetime import datetime

from sqlalchemy import Text, DateTime, String, event
from sqlalchemy.orm import Mapped, mapped_column
from slugify import slugify

from app.infrastucture.database import Base


class CategoryModel(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(256))
    slug: Mapped[str] = mapped_column(String, unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_published: Mapped[bool] = mapped_column(default=true)


@event.listens_for(CategoryModel, "before_insert")
def get_slug(_, __, category_obj):
    if not category_obj.slug and category_obj.title:
        category_obj.slug = slugify(category_obj.title)
