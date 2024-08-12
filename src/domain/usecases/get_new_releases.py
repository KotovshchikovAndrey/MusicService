from domain.common.mappers import map_to_album_info_dto
from domain.dtos.inputs import GetNewReleasesDto
from domain.dtos.outputs import AlbumInfoDto
from domain.usecases.base import BaseUseCase
from domain.utils.uow import UnitOfWork


class GetNewReleasesUseCase(BaseUseCase[GetNewReleasesDto, list[AlbumInfoDto]]):
    _uow: UnitOfWork

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, data: GetNewReleasesDto) -> list[AlbumInfoDto]:
        async with self._uow as uow:
            albums = await uow.albums.get_new_releases(limit=data.limit)
            return [map_to_album_info_dto(album) for album in albums]
