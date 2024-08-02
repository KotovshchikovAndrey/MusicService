from sqlalchemy.ext.asyncio import AsyncSession
from domain.entities.playlist import Playlist
from domain.repositories.playlist import PlaylistRepository


class PlaylistSqlRepository(PlaylistRepository):
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_user_playlists(
        self, user_oid: str, limit: int, offset: int
    ) -> list[Playlist]: ...

    async def get_user_playlist(
        self, user_oid: str, playlist_oid: str
    ) -> Playlist | None: ...

    async def upsert(self, playlist: Playlist) -> None: ...

    async def remove_by_oid(self, playlist_oid: str) -> None: ...
