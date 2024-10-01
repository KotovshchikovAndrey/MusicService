import asyncio
from typing import Iterable
import pytest
from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
    create_async_engine,
)

from adapters.driven.sql.connection import SQLDatabaseConnection
from adapters.driven.sql.models import Base as BaseModel
from adapters.driven.sql.models.album import Album as AlbumModel
from adapters.driven.sql.models.artist import Artist as ArtistModel
from adapters.driven.sql.models.track import Track as TrackModel
from adapters.driven.sql.models.user import User as UserModel
from config.settings import settings
from domain.models.entities.album import Album
from domain.models.entities.artist import Artist
from domain.models.entities.track import Track
from domain.models.entities.user import User


async def create_tables(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)


async def drop_tables(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)


async def close_all_sessions_in_scoped_registry(
    scoped_session: async_scoped_session[AsyncSession],
) -> None:
    """Close all sessions which has been registered in AsyncScopedSession registry"""

    db_sessions: Iterable[AsyncSession] = scoped_session.registry.registry.values()
    async with asyncio.TaskGroup() as tg:
        for db_session in db_sessions:
            tg.create_task(db_session.close())


@pytest.fixture(scope="session")
async def database():
    database = SQLDatabaseConnection(
        connection_url=settings.database.get_test_connection_url(),
        echo=False,
    )

    yield database
    await database.close()


@pytest.fixture(scope="session", autouse=True)
async def prepare_database(
    mock_album: Album,
    mock_track: Track,
    mock_artist: Artist,
    mock_user: User,
):
    engine = create_async_engine(settings.database.get_test_connection_url())
    await create_tables(engine)

    user_model = UserModel(
        id=mock_user.id,
        email=mock_user.email.value,
        is_active=mock_user.is_active,
        created_at=mock_user.created_at.replace(tzinfo=None),
    )

    album_model = AlbumModel(
        id=mock_album.id,
        title=mock_album.title.value,
        cover_url=mock_album.cover_url.value,
        created_at=mock_album.created_at.replace(tzinfo=None),
    )

    track_model = TrackModel(
        id=mock_track.id,
        title=mock_track.title.value,
        album_id=mock_track.album_id,
        audio_url=mock_track.audio_url.value,
        duration=mock_track.duration.value,
    )

    artist_model = ArtistModel(
        id=mock_artist.id,
        nickname=mock_artist.nickname.value,
        avatar_url=mock_artist.avatar_url.value,
    )

    session = async_sessionmaker(engine)()
    session.add_all([user_model, album_model, track_model, artist_model])
    await session.commit()
    await session.close()

    yield
    await engine.dispose()


@pytest.fixture(scope="function")
async def session(database: SQLDatabaseConnection):
    session = database.get_session()
    try:
        yield session
    except:
        await session.rollback()
    finally:
        await close_all_sessions_in_scoped_registry(session)
