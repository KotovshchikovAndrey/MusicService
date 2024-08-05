from domain.entities.artist import Artist
from domain.entities.track import Track
from domain.repositories.track import TrackRepository


class MockedTrackRepository(TrackRepository):
    _tracks: dict[str, Track]

    def __init__(self, tracks: list[Track]) -> None:
        self._tracks = {track.oid.value: track for track in tracks}

    async def get_by_oid(self, track_oid: str) -> Track | None:
        return self._tracks.get(track_oid, None)

    async def get_top_for_all_time(self, limit: int) -> list[Track]:
        raise NotImplementedError

    async def get_top_for_day(self, limit: int) -> list[Track]:
        raise NotImplementedError

    async def upsert(self, track: Track) -> None:
        self._tracks[track.oid.value] = track

    async def set_track_artists(self, track_oid: str, *artists: Artist) -> None:
        track = await self.get_by_oid(track_oid)
        track = Track(
            oid=track.oid,
            title=track.title,
            album_oid=track.album_oid,
            audio_url=track.audio_url,
            duration=track.duration,
            listens=track.listens,
            artists=artists,
        )

        self._tracks[track.oid.value] = track

    async def increment_listens(self, track_oid: str) -> None:
        raise NotImplementedError
