from uuid import uuid4

import pytest

from domain.models.entities.artist import Artist
from domain.ports.driven.blob_storage import BlobStorage
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driven.file_downloader import FileDownloader
from domain.ports.driving.artist_registration import RegisterArtistDTO
from domain.usecases.register_artist import RegisterArtistUseCaseImpl


class TestRegisterArtistUseCase:
    @pytest.mark.parametrize(
        "data",
        (
            RegisterArtistDTO(
                user_id=uuid4(),
                nickname="Andrew",
                avatar_url="https://example.com/avatar.png",
            ),
        ),
    )
    async def test_execute_successfully(
        self,
        data: RegisterArtistDTO,
        mock_uow: UnitOfWork,
        mock_file_downloader: FileDownloader,
        mock_blob_storage: BlobStorage,
    ) -> None:
        mock_uow.artists.get_by_id.return_value = None
        usecase = RegisterArtistUseCaseImpl(
            uow=mock_uow,
            file_downloader=mock_file_downloader,
            blob_storage=mock_blob_storage,
        )

        artist_id = await usecase.execute(data)
        assert artist_id == data.user_id

    async def test_execute_when_artist_exists(
        self,
        mock_artist: Artist,
        mock_uow: UnitOfWork,
        mock_file_downloader: FileDownloader,
        mock_blob_storage: BlobStorage,
    ) -> None:
        mock_uow.artists.get_by_id.return_value = mock_artist
        data = RegisterArtistDTO(
            user_id=mock_artist.id,
            nickname="Andrew",
            avatar_url="https://example.com/avatar.png",
        )

        usecase = RegisterArtistUseCaseImpl(
            uow=mock_uow,
            file_downloader=mock_file_downloader,
            blob_storage=mock_blob_storage,
        )

        artist_id = await usecase.execute(data)
        assert artist_id == mock_artist.id
