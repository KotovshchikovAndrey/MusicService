from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.playlist import Playlist, PlaylistInfo
from domain.repositories.playlist import PlaylistRepository


class PlaylistSqlRepository(PlaylistRepository):
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_user_playlists(
        self, user_id: UUID, limit: int, offset: int
    ) -> list[Playlist]:
        raise NotImplementedError

    async def get_user_playlist_info(
        self, user_id: UUID, playlist_id: UUID
    ) -> PlaylistInfo | None:
        raise NotImplementedError

    async def save(self, playlist: Playlist) -> None:
        raise NotImplementedError

    async def remove_by_id(self, playlist_id: UUID) -> None:
        raise NotImplementedError
