from datetime import UTC, datetime
from dataclasses import dataclass, field

from domain.entities.artist import Artist
from domain.entities.base import BaseEntity
from domain.entities.track import Track

from domain.exceptions.permission_denied import PermissionDeniedException
from domain.values.cover_url import CoverUrl
from domain.values.title import Title


@dataclass(eq=False, kw_only=True, slots=True)
class Album(BaseEntity):
    title: Title
    cover_url: CoverUrl
    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC).replace(tzinfo=None)
    )
    tracks: set[Track] = field(default_factory=set)

    def set_title(self, title: str, my_oid: str) -> None:
        if not self._is_artist(my_oid):
            raise PermissionDeniedException()

        self.title = Title(title)

    def set_cover(self, url: str, my_oid: str) -> None:
        if not self._is_artist(my_oid):
            raise PermissionDeniedException()

        self.cover_url = CoverUrl(url)

    def _is_artist(self, oid: str) -> bool:
        for artist in self._get_artists():
            if artist.oid == oid:
                return True

        return False

    def _get_artists(self) -> set[Artist]:
        artists = set()
        for track in self.tracks:
            artists.update(track.artists)

        return artists
