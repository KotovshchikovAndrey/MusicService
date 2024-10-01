from domain.models.entities.artist import Artist
from domain.models.entities.track import PopularTrack
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driving.chart_getting import GetChartDTO
from domain.usecases.get_chart import GetChartUseCaseImpl


class TestGetChartUseCase:
    async def test_get_chart_correct_output(
        self,
        mock_uow: UnitOfWork,
        mock_popular_track: PopularTrack,
        mock_artist: Artist,
    ) -> None:
        mock_uow.tracks.get_most_popular_for_period.return_value = [mock_popular_track]
        usecase = GetChartUseCaseImpl(uow=mock_uow)
        tracks = await usecase.execute(GetChartDTO(limit=1))

        assert len(tracks) == 1
        for track in tracks:
            assert track.id == mock_popular_track.id
            assert track.title == mock_popular_track.title
            assert track.audio_url == mock_popular_track.audio_url
            assert track.cover_url == mock_popular_track.cover_url
            assert track.duration == mock_popular_track.duration

            for artist in track.artists:
                assert artist.id == mock_artist.id
                assert artist.nickname == mock_artist.nickname
