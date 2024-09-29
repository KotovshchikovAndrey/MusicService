from domain.models.entities.artist import Artist
from domain.models.entities.track import PopularTrack
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driving.chart_getting import GetChartDTO
from domain.usecases.get_chart import GetChartUseCaseImpl


class TestGetChartUseCase:
    async def test_get_chart_correct_output(
        self,
        uow_mock: UnitOfWork,
        popular_track_mock: PopularTrack,
        artist_mock: Artist,
    ) -> None:
        usecase = GetChartUseCaseImpl(uow=uow_mock)
        tracks = await usecase.execute(GetChartDTO(limit=1))

        assert len(tracks) == 1
        for track in tracks:
            assert track.id == popular_track_mock.id
            assert track.title == popular_track_mock.title
            assert track.audio_url == popular_track_mock.audio_url
            assert track.cover_url == popular_track_mock.cover_url
            assert track.duration == popular_track_mock.duration

            for artist in track.artists:
                assert artist.id == artist_mock.id
                assert artist.nickname == artist_mock.nickname
