from unittest.mock import AsyncMock, MagicMock

import pytest

from domain.entities.artist import Artist
from domain.repositories.artist import ArtistRepository


@pytest.fixture(scope="package")
def artist_repository_mock(artist_mock: Artist) -> ArtistRepository:
    repository = MagicMock(spec=ArtistRepository)
    repository.get_by_oid = AsyncMock(return_value=artist_mock)
    repository.filter_by_oids = AsyncMock(return_value=[artist_mock])
    repository.upsert = AsyncMock()
    return repository
