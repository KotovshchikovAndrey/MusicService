import hashlib
from typing import NewType

from domain.dtos.album import CreateAlbumDto
from domain.entities.album import Album
from domain.usecases.base import BaseUseCase
from domain.utils.blob import BlobStorage
from domain.utils.moderation import ModerationServiceAdapter
from domain.utils.uow import UnitOfWork

AlbumOid = NewType("AlbumOid", str)


class CreateAlbumUseCase(BaseUseCase[CreateAlbumDto, AlbumOid]):
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

    async def execute(self, data: CreateAlbumDto) -> AlbumOid:
        cover = await self._moderation_service.upload_approved_cover(
            filename=data.cover_filename
        )

        hashed_cover = hashlib.sha256(cover.getvalue()).hexdigest()
        cover_url = f"/{hashed_cover}.{data.cover_filename.split(".")[-1]}"
        album = Album.create(title=data.title, cover_url=cover_url)

        async with self._uow as uow:
            await uow.albums.upsert(album)
            await self._blob_storage.put(blob_url=cover_url, blob=cover)
            await uow.commit()

        return album.oid.value
