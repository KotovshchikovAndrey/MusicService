from typing import Protocol
from uuid import UUID

from domain.entities.playlist import Playlist, PlaylistInfo


class PlaylistRepository(Protocol):
    async def get_user_playlists(
        self, user_id: UUID, limit: int, offset: int
    ) -> list[Playlist]: ...

    async def get_user_playlist_info(
        self, user_id: UUID, playlist_id: UUID
    ) -> PlaylistInfo | None: ...

    async def save(self, playlist: Playlist) -> None: ...

    async def remove_by_id(self, playlist_id: UUID) -> None: ...
