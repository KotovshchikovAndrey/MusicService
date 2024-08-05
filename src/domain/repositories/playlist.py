from typing import Protocol

from domain.entities.playlist import Playlist


class PlaylistRepository(Protocol):
    async def get_user_playlists(
        self, user_oid: str, limit: int, offset: int
    ) -> list[Playlist]: ...

    async def get_user_playlist(
        self, user_oid: str, playlist_oid: str
    ) -> Playlist | None: ...

    async def upsert(self, playlist: Playlist) -> None: ...

    async def remove_by_oid(self, playlist_oid: str) -> None: ...
