import hashlib
from uuid import UUID

from domain.dtos.inputs import CreateAlbumDto
from domain.factories.album import AlbumFactory
from domain.usecases.base import BaseUseCase
from domain.utils.blob_storage import BlobStorage
from domain.utils.moderation import ModerationServiceAdapter
from domain.utils.uow import UnitOfWork

type AlbumId = UUID


class CreateAlbumUseCase(BaseUseCase[CreateAlbumDto, AlbumId]):
    _uow: UnitOfWork
    _blob_storage: BlobStorage
    _moderation_service: ModerationServiceAdapter

    def __init__(
        self,
        uow: UnitOfWork,
        blob_storage: BlobStorage,
        moderation_service: ModerationServiceAdapter,
    ) -> None:
        self._uow = uow
        self._blob_storage = blob_storage
        self._moderation_service = moderation_service

    async def execute(self, data: CreateAlbumDto) -> AlbumId:
        cover = await self._moderation_service.download_approved_cover(
            filename=data.cover_filename
        )

        hashed_cover = hashlib.sha256(cover.getvalue()).hexdigest()
        cover_url = f"/{hashed_cover}.{data.cover_filename.split(".")[-1]}"

        album_factory = AlbumFactory(title=data.title, cover_url=cover_url)
        album = album_factory.create()

        async with self._uow as uow:
            await uow.albums.upsert(album)
            await self._blob_storage.put(blob_url=cover_url, blob=cover)
            await uow.commit()

        return album.id
