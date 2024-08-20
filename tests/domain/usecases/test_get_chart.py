from domain.dtos.inputs import GetChartDto
from domain.entities.track import ChartedTrack
from domain.usecases.get_chart import GetChartUseCase
from domain.utils.uow import UnitOfWork


class TestGetChartUseCase:
    async def test_get_chart_correct_output(
        self, uow_mock: UnitOfWork, charted_track_mock: ChartedTrack
    ) -> None:
        usecase = GetChartUseCase(uow=uow_mock)
        tracks = await usecase.execute(GetChartDto(limit=1))

        assert len(tracks) == 1
        assert tracks[0].id == charted_track_mock.id
        assert tracks[0].title == charted_track_mock.title.value
        assert tracks[0].audio_url == charted_track_mock.audio_url.value
        assert tracks[0].cover_url == charted_track_mock.cover_url.value
        assert tracks[0].duration == charted_track_mock.duration.value

        for index, artist in enumerate(tracks[0].artists):
            artist.id == charted_track_mock.artists[index].id
            artist.nickname == charted_track_mock.artists[index].nickname.value
