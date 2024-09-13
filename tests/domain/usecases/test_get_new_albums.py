from domain.models.entities.album import AlbumInfo
from domain.models.entities.artist import Artist
from domain.models.entities.track import Track
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driving.getting_new_albums import GetNewAlbumsDto
from domain.usecases.get_new_albums import GetNewAlbumsUseCaseImpl


class TestGetNewAlbumsUseCase:
    async def test_get_new_albums_correct_output(
        self,
        uow_mock: UnitOfWork,
        album_info_mock: AlbumInfo,
        track_mock: Track,
        artist_mock: Artist,
    ) -> None:
        usecase = GetNewAlbumsUseCaseImpl(uow=uow_mock)
        albums = await usecase.execute(GetNewAlbumsDto(limit=1))

        assert len(albums) == 1
        for album in albums:
            assert album.id == album_info_mock.id
            assert album.title == album_info_mock.title
            assert album.cover_url == album_info_mock.cover_url
            assert album.created_at == album_info_mock.created_at

            for track in album.tracks:
                assert track.id == track_mock.id
                assert track.title == track_mock.title
                assert track.audio_url == track_mock.audio_url
                assert track.duration == track_mock.duration

                for artist in track.artists:
                    assert artist.id == artist_mock.id
                    assert artist.nickname == artist_mock.nickname
