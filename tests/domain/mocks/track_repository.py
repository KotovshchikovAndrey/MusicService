from unittest.mock import AsyncMock, MagicMock

import pytest

from domain.entities.track import ChartedTrack, Track
from domain.repositories.track import TrackRepository


@pytest.fixture(scope="package")
def track_repository_mock(
    track_mock: Track,
    charted_track_mock: ChartedTrack,
) -> TrackRepository:
    repository = MagicMock(spec=TrackRepository)
    repository.get_by_oid = AsyncMock(return_value=track_mock)
    repository.upsert = AsyncMock()
    repository.get_top_chart_for_period = AsyncMock(return_value=[charted_track_mock])
    return repository
