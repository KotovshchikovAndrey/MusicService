import math

from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driving.artists_getting import (
    GetArtistsDTO,
    GetArtistsUseCase,
    PaginatedArtists,
)


class GetArtistsUseCaseImpl(GetArtistsUseCase):
    _uow: UnitOfWork
    _limit: int

    def __init__(self, uow: UnitOfWork, limit: int) -> None:
        self._uow = uow
        self._limit = limit

    async def execute(self, data: GetArtistsDTO) -> PaginatedArtists:
        async with self._uow as uow:
            offset = (data.page - 1) * self._limit
            artists = await uow.artists.get_list(limit=self._limit, offset=offset)
            total_count = await uow.artists.get_total_count()
            total_pages = math.ceil(total_count / self._limit)

            return PaginatedArtists(
                count=len(artists),
                total_count=total_count,
                current_page=data.page,
                total_pages=total_pages,
                prev_page=data.page - 1 if data.page > 1 else None,
                next_page=data.page + 1 if data.page < total_pages else None,
                artists=artists,
            )
