from datetime import datetime

from sqlalchemy import String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastucture.database import Base


class PostModel(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_username: Mapped[str] = mapped_column(ForeignKey("users.username", ondelete="CASCADE"))
    category_slug: Mapped[str] = mapped_column(ForeignKey("categories.slug", ondelete="SET NULL"))
    image_url: Mapped[str | None] = mapped_column(String)
    location_name: Mapped[str] = mapped_column(ForeignKey("locations.name", ondelete="SET NULL"))
    title: Mapped[str] = mapped_column(String(256))
    text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    publicated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_published: Mapped[bool] = mapped_column(default=True)
