from domain.entities.album import Album
from domain.repositories.album import AlbumRepository


class MockedAlbumRepository(AlbumRepository):
    _albums: dict[str, Album]

    def __init__(self, albums: list[Album]) -> None:
        self._albums = {album.oid.value: album for album in albums}

    async def get_new_releases(self, limit: int) -> list[Album]:
        raise NotImplementedError

    async def get_by_oid(
        self, album_oid: str, fetch_tracks: bool = False
    ) -> Album | None:
        return self._albums.get(album_oid, None)

    async def upsert(self, album: Album) -> None:
        self._albums[album.oid.value] = album
