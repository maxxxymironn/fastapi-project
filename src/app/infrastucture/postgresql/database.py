from contextlib import asynccontextmanager

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from app.core.config import settings


class Database:
    def __init__(self):
        self._engine = create_async_engine(settings.postgres_url)
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
            class_=AsyncSession
        )

    @asynccontextmanager
    async def session(self):
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise


db = Database()
metadata = MetaData(schema=settings.POSTGRES_SCHEMA)
Base = declarative_base()
