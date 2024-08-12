from unittest.mock import AsyncMock, MagicMock

import pytest

from domain.entities.album import Album, AlbumInfo
from domain.repositories.album import AlbumRepository


@pytest.fixture(scope="package")
def album_repository_mock(
    album_mock: Album,
    album_info_mock: AlbumInfo,
) -> AlbumRepository:
    repository = MagicMock(spec=AlbumRepository)
    repository.get_by_oid = AsyncMock(return_value=album_mock)
    repository.upsert = AsyncMock()
    repository.get_new_releases = AsyncMock(return_value=[album_info_mock])
    return repository
