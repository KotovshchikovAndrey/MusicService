import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from adapters.driven.sql.models import BaseModel
from adapters.driven.sql.models.album import AlbumModel
from adapters.driven.sql.models.artist import ArtistModel
from adapters.driven.sql.models.track import TrackModel
from config.settings import settings
from domain.entities.album import Album
from domain.entities.artist import Artist
from domain.entities.track import Track


@pytest.fixture
async def session():
    engine = create_async_engine(settings.database.get_test_connection_url())
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)

    session = async_sessionmaker(engine)()
    yield session
    await session.close()


@pytest.fixture(autouse=True)
async def prepare_database(
    session: AsyncSession,
    album_mock: Album,
    track_mock: Track,
    artist_mock: Artist,
):
    album_model = AlbumModel(
        id=album_mock.id,
        title=album_mock.title.value,
        cover_url=album_mock.cover_url.value,
        created_at=album_mock.created_at.replace(tzinfo=None),
    )

    track_model = TrackModel(
        id=track_mock.id,
        title=track_mock.title.value,
        album_id=track_mock.album_id,
        audio_url=track_mock.audio_url.value,
        duration=track_mock.duration.value,
        listens=track_mock.listens.value,
    )

    artist_model = ArtistModel(
        id=artist_mock.id,
        nickname=artist_mock.nickname.value,
        avatar_url=artist_mock.avatar_url.value,
    )

    session.add_all([album_model, track_model, artist_model])
    await session.commit()
