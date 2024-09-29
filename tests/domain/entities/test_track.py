import pytest

from domain.models.builders.track import TrackBuilder
from domain.models.entities.album import Album


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
        new_track = (
            TrackBuilder()
            .set_title(title=title)
            .set_album(album_id=album_mock.id)
            .set_audio(audio_url=audio_url)
            .set_duration(duration=duration)
            .build()
        )

        assert new_track.id is not None
        assert new_track.title.value == title
        assert new_track.duration.value == duration
        assert new_track.audio_url.value == audio_url
        assert new_track.album_id == album_mock.id
