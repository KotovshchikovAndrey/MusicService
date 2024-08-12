from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from adapters.sql.models import BaseModel
from config.settings import settings


@pytest.fixture(scope="package")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(settings.database.get_test_connection_url())
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)

    session = async_sessionmaker(engine)()
    yield session
    await session.close()
