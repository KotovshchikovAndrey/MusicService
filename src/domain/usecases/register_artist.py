from domain.exceptions.artist import ArtistExists
from domain.models.builders.artist import ArtistBuilder
from domain.ports.driven.blob_storage import BlobStorage
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driven.distribution_service import DistributionServiceAdapter
from domain.ports.driving.registering_artists import (
    RegisterArtistDto,
    RegisterArtistUseCase,
)


class RegisterArtistUseCaseImpl(RegisterArtistUseCase):
    _uow: UnitOfWork
    _blob_storage: BlobStorage
    _distribution_service: DistributionServiceAdapter

    def __init__(
        self,
        uow: UnitOfWork,
        blob_storage: BlobStorage,
        distribution_service: DistributionServiceAdapter,
    ) -> None:
        self._uow = uow
        self._blob_storage = blob_storage
        self._distribution_service = distribution_service

    async def execute(self, data: RegisterArtistDto) -> None:
        async with self._uow as uow:
            artist = await uow.artists.get_by_id(data.id)
            if artist is not None:
                raise ArtistExists()

        avatar = await self._distribution_service.download_file(data.avatar_download_url)
        artist = (
            ArtistBuilder()
            .set_user(user_id=data.user_id)
            .set_nickname(nickname=data.nickname)
            .set_avatar(avatar_url=avatar.url)
            .build()
        )

        await self._blob_storage.put(blob_url=artist.avatar_url.value, blob=avatar)
        async with self._uow as uow:
            await uow.artists.save(artist)
            await uow.commit()
