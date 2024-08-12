from domain.dtos.inputs import GetNewReleasesDto
from domain.entities.album import AlbumInfo
from domain.entities.artist import Artist
from domain.entities.track import Track
from domain.usecases.get_new_releases import GetNewReleasesUseCase
from domain.utils.uow import UnitOfWork


class TestGetNewReleasesUseCase:
    async def test_get_new_releases_correct_output(
        self,
        uow_mock: UnitOfWork,
        album_info_mock: AlbumInfo,
        track_mock: Track,
        artist_mock: Artist,
    ) -> None:
        usecase = GetNewReleasesUseCase(uow=uow_mock)
        albums = await usecase.execute(GetNewReleasesDto(limit=1))

        assert len(albums) == 1
        assert len(albums[0].tracks) == 1
        assert albums[0].oid == album_info_mock.oid.value
        assert albums[0].title == album_info_mock.title.value
        assert albums[0].cover_url == album_info_mock.cover_url.value
        assert albums[0].created_at == album_info_mock.created_at.isoformat()

        for track in albums[0].tracks:
            assert track.oid == track_mock.oid.value
            assert track.title == track_mock.title.value
            assert track.audio_url == track_mock.audio_url.value
            assert track.duration == track_mock.duration.value

            for artist in track.artists:
                assert artist.oid == artist_mock.oid.value
                assert artist.nickname == artist_mock.nickname.value
