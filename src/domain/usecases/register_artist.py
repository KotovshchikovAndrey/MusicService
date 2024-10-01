from uuid import UUID

from domain.models.builders.artist import ArtistBuilder
from domain.ports.driven.blob_storage import BlobStorage
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driven.file_downloader import FileDownloader
from domain.ports.driving.artist_registration import (
    RegisterArtistDTO,
    RegisterArtistUseCase,
)
from domain.usecases.mixins.file_manager_mixin import FileManagerMixin


class RegisterArtistUseCaseImpl(FileManagerMixin, RegisterArtistUseCase):
    _uow: UnitOfWork
    _blob_storage: BlobStorage
    _file_downloader: FileDownloader

    def __init__(
        self,
        uow: UnitOfWork,
        blob_storage: BlobStorage,
        file_downloader: FileDownloader,
    ) -> None:
        self._uow = uow
        self._blob_storage = blob_storage
        self._file_downloader = file_downloader

    async def execute(self, data: RegisterArtistDTO) -> UUID:
        async with self._uow as uow:
            artist = await uow.artists.get_by_id(data.user_id)
            if artist is not None:
                return artist.id

        avatar_url = await self._transfer_file_to_blob_storage(url=data.avatar_url)
        artist = (
            ArtistBuilder()
            .set_id(user_id=data.user_id)
            .set_nickname(nickname=data.nickname)
            .set_avatar(avatar_url=avatar_url)
            .build()
        )

        async with self._uow as uow:
            await uow.artists.save(artist)
            await uow.commit()

        return artist.id
