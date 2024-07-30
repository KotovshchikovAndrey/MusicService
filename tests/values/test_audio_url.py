import pytest

from domain.values.audio_url import AudioUrl


class TestAudioUrl:
    @pytest.mark.parametrize(
        "value",
        (
            "/audio.png",
            "audio.mp3",
            "/",
            "/audio.",
            f"/audio{"A" * 9_999}.aac",
            "/audio.mp3something",
        ),
    )
    async def test_invalid_audio_url(self, value: str) -> None:
        with pytest.raises(ValueError):
            AudioUrl(value)

    @pytest.mark.parametrize(
        "value",
        (
            "/audio.mp3",
            "/audio.aac",
            "/audio.flac",
            "/test_audio.mp3",
            "/test-audio.mp3",
        ),
    )
    async def test_valid_audio_url(self, value: str) -> None:
        audio_url = AudioUrl(value)
        assert audio_url.value == value

