from unittest.mock import AsyncMock
from domain.models.entities.album import AlbumInfo
from domain.models.entities.artist import Artist
from domain.models.entities.track import Track
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driving.albums_getting import GetAlbumsDTO
from domain.usecases.get_albums import GetAlbumsUseCaseImpl


class TestGetAlbumsUseCase:
    async def test_get_new_albums_correct_output(
        self,
        mock_uow: UnitOfWork,
        mock_album_info: AlbumInfo,
        mock_track: Track,
        mock_artist: Artist,
    ) -> None:
        mock_uow.albums.get_new_releases = AsyncMock(return_value=[mock_album_info])
        usecase = GetAlbumsUseCaseImpl(uow=mock_uow)
        albums = await usecase.execute(GetAlbumsDTO(limit=1))

        assert len(albums) == 1
        for album in albums:
            assert album.id == mock_album_info.id
            assert album.title == mock_album_info.title
            assert album.cover_url == mock_album_info.cover_url
            assert album.created_at == mock_album_info.created_at

            for track in album.tracks:
                assert track.id == mock_track.id
                assert track.title == mock_track.title
                assert track.audio_url == mock_track.audio_url
                assert track.duration == mock_track.duration

                for artist in track.artists:
                    assert artist.id == mock_artist.id
                    assert artist.nickname == mock_artist.nickname
