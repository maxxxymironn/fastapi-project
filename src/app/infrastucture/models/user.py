from datetime import datetime

from sqlalchemy import Text, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastucture.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(128), unique=True)
    password: Mapped[str] = mapped_column(String(128))