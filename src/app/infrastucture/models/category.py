from enum import unique
from datetime import datetime

from sqlalchemy import Text, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastucture.database import Base


class CategoryModel(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(256))
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_published: Mapped[bool] = mapped_column(default=true)
