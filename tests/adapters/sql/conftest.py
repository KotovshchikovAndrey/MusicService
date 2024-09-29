import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

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


@pytest.fixture(scope="function")
async def session():
    engine = create_async_engine(settings.database.get_test_connection_url())
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)

    session = async_sessionmaker(engine)()
    yield session
    await session.close()


@pytest.fixture(scope="function", autouse=True)
async def prepare_database(
    session: AsyncSession,
    album_mock: Album,
    track_mock: Track,
    artist_mock: Artist,
    user_mock: User,
):
    user_model = UserModel(
        id=user_mock.id,
        email=user_mock.email.value,
        is_active=user_mock.is_active,
        created_at=user_mock.created_at.replace(tzinfo=None),
    )

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
    )

    artist_model = ArtistModel(
        id=artist_mock.id,
        nickname=artist_mock.nickname.value,
        avatar_url=artist_mock.avatar_url.value,
    )

    session.add_all([user_model, album_model, track_model, artist_model])
    await session.commit()
