from sqlalchemy.ext.asyncio import AsyncSession

from adapters.sql.repositories.album import AlbumSqlRepository
from domain.entities.album import Album


class TestAlbumSqlRepository:
    async def test_get_by_id(self, session: AsyncSession, album_mock: Album) -> None:
        repository = AlbumSqlRepository(session=session)
        album = await repository.get_by_id(album_mock.id.hex)

        assert album is not None
        assert album.id == album_mock.id
        assert album.title == album_mock.title
        assert album.cover_url == album_mock.cover_url
        assert album.created_at == album_mock.created_at
