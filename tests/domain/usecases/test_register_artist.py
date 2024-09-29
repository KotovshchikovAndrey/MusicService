from uuid import uuid4

from domain.models.entities.artist import Artist
from domain.ports.driven.blob_storage import BlobStorage
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driven.file_downloader import FileDownloader
from domain.ports.driving.artist_registration import RegisterArtistDTO
from domain.usecases.register_artist import RegisterArtistUseCaseImpl


class TestRegisterArtistUseCase:
    async def test_execute_successfully(
        self,
        uow_mock: UnitOfWork,
        file_downloader_mock: FileDownloader,
        blob_storage_mock: BlobStorage,
    ) -> None:
        data = RegisterArtistDTO(
            user_id=uuid4(),
            nickname="Andrew",
            avatar_download_url="/avatar.png",
        )

        uow_mock.artists.get_by_id.return_value = None
        usecase = RegisterArtistUseCaseImpl(
            uow=uow_mock,
            file_downloader=file_downloader_mock,
            blob_storage=blob_storage_mock,
        )

        artist_id = await usecase.execute(data)
        assert artist_id == data.user_id

    async def test_execute_when_artist_exists(
        self,
        artist_mock: Artist,
        uow_mock: UnitOfWork,
        file_downloader_mock: FileDownloader,
        blob_storage_mock: BlobStorage,
    ) -> None:
        data = RegisterArtistDTO(
            user_id=artist_mock.id,
            nickname="Andrew",
            avatar_download_url="/avatar.png",
        )

        usecase = RegisterArtistUseCaseImpl(
            uow=uow_mock,
            file_downloader=file_downloader_mock,
            blob_storage=blob_storage_mock,
        )

        artist_id = await usecase.execute(data)
        assert artist_id == data.user_id
