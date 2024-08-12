import math

from domain.common.mappers import map_to_artist_dto
from domain.dtos.inputs import GetArtistsDto
from domain.dtos.outputs import ArtistListDto
from domain.usecases.base import BaseUseCase
from domain.utils.uow import UnitOfWork


class GetArtistsUseCase(BaseUseCase[GetArtistsDto, ArtistListDto]):
    _uow: UnitOfWork
    _limit: int

    def __init__(self, uow: UnitOfWork, limit: int) -> None:
        self._uow = uow
        self._limit = limit

    async def execute(self, data: GetArtistsDto) -> ArtistListDto:
        async with self._uow as uow:
            offset = (data.page - 1) * self._limit
            artists = await uow.artists.get_list(limit=self._limit, offset=offset)

            artist_dtos = [map_to_artist_dto(artist) for artist in artists]
            total_count = await uow.artists.get_total_count()
            total_pages = math.ceil(total_count / self._limit)

            return ArtistListDto(
                count=len(artist_dtos),
                total_count=total_count,
                current_page=data.page,
                total_pages=total_pages,
                prev_page=data.page - 1 if data.page > 1 else None,
                next_page=data.page + 1 if data.page < total_pages else None,
                artists=artist_dtos,
            )
