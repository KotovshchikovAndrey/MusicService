import pytest
from domain.entities.album import Album
from domain.entities.artist import Artist
from domain.entities.track import Track

from domain.values.audio_url import AudioUrl
from domain.values.duration import Duration
from domain.values.title import Title


class TestTrack:
    @pytest.mark.parametrize(
        "title, duration, audio_url",
        (
            (
                "In The End (Dj Dark & Nesco Remix)",
                3 * 60,
                "/audio.mp3",
            ),
            (
                "Setting Sun",
                2 * 60 + 50,
                "/audio.aac",
            ),
            (
                "After Dark",
                4 * 60 + 18,
                "/audio.flac",
            ),
        ),
    )
    async def test_create_track_success(
        self,
        title: str,
        duration: int,
        audio_url: str,
        artist: Artist,
        album: Album,
    ) -> None:
        new_track = Track(
            album_oid=album.oid,
            title=Title(title),
            duration=Duration(duration),
            audio_url=AudioUrl(audio_url),
            artists=(artist,),
        )

        assert new_track.oid is not None
        assert new_track.title.value == title
        assert new_track.duration.value == duration
        assert new_track.audio_url.value == audio_url
        assert new_track.album_oid == album.oid

        assert len(new_track.artists) == 1
        assert new_track.artists[0] == artist
