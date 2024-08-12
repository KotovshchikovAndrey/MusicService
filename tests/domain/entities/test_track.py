import pytest

from domain.entities.album import Album
from domain.factories.track import TrackFactory


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
        album_mock: Album,
    ) -> None:
        track_factory = TrackFactory(
            album_oid=album_mock.oid.value,
            audio_url=audio_url,
            duration=duration,
            title=title,
        )

        new_track = track_factory.create()

        assert new_track.oid is not None
        assert new_track.title.value == title
        assert new_track.duration.value == duration
        assert new_track.audio_url.value == audio_url
        assert new_track.album_oid == album_mock.oid
        assert new_track.listens.value == 0
