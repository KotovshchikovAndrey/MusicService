from asyncio import current_task
import asyncio
from typing import Iterable, Self

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)


class SQLDatabaseConnection:
    _instance: Self | None = None

    _engine: AsyncEngine
    _session_factory: async_sessionmaker[AsyncSession]

    def __new__(
        cls: type["SQLDatabaseConnection"], *args, **kwargs
    ) -> "SQLDatabaseConnection":
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, connection_url: str, echo: bool) -> None:
        self._engine = create_async_engine(url=connection_url, echo=echo)
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_session(self) -> async_scoped_session[AsyncSession]:
        session = async_scoped_session(
            session_factory=self._session_factory,
            scopefunc=current_task,
        )

        return session

    async def close(self) -> None:
        await self._engine.dispose()
