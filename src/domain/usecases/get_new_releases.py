from domain.dtos.album import AlbumDto, GetNewReleasesDto
from domain.mappers.album import map_to_album_dto
from domain.utils.uow import UnitOfWork
from domain.usecases.base import BaseUseCase


class GetNewReleasesUseCase(BaseUseCase[GetNewReleasesDto, list[AlbumDto]]):
    _uow: UnitOfWork

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, data: GetNewReleasesDto) -> list[AlbumDto]:
        async with self._uow as uow:
            albums = await uow.albums.get_new(limit=data.limit, offset=data.offset)
            return [map_to_album_dto(album) for album in albums]
