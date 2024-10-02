from domain.models.entities.album import AlbumInfo
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driving.albums_getting import GetAlbumsDTO, GetAlbumsUseCase


class GetAlbumsUseCaseImpl(GetAlbumsUseCase):
    _uow: UnitOfWork

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, data: GetAlbumsDTO) -> list[AlbumInfo]:
        async with self._uow as uow:
            albums = await uow.albums.get_new_releases(limit=data.limit)
            return albums
