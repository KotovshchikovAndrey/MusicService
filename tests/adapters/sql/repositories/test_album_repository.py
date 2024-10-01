from sqlalchemy.ext.asyncio import AsyncSession

from adapters.driven.sql.repositories.album import AlbumSQLRepository
from domain.models.entities.album import Album


class TestAlbumSQLRepository:
    async def test_get_by_id(self, session: AsyncSession, mock_album: Album) -> None:
        repository = AlbumSQLRepository(session=session)
        album = await repository.get_by_id(mock_album.id)

        assert album is not None
        assert album.id == mock_album.id
        assert album.title == mock_album.title
        assert album.cover_url == mock_album.cover_url
        assert album.created_at == mock_album.created_at
