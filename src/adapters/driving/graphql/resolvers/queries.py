import strawberry

from adapters.driving.graphql.common import exceptions
from adapters.driving.graphql.mappers.responses import (
    map_to_artists_success,
    map_to_chart_success,
    map_to_new_albums_success,
)
from adapters.driving.graphql.models.responses import (
    ArtistsResponse,
    ChartResponse,
    NewAlbumsResponse,
)
from config.ioc_container import container
from domain.ports.driving.getting_artists import GetArtistsDto, GetArtistsUseCase
from domain.ports.driving.getting_chart import GetChartDto, GetChartUseCase
from domain.ports.driving.getting_new_albums import GetNewAlbumsDto, GetNewAlbumsUseCase


@strawberry.type
class Query:
    @strawberry.field
    async def get_chart(self, limit: int) -> ChartResponse:
        if limit <= 0:
            return exceptions.InvalidLimitParamException()

        usecase = container.resolve(GetChartUseCase)
        output = await usecase.execute(GetChartDto(limit=limit))
        return map_to_chart_success(output)

    @strawberry.field
    async def get_new_albums(self, limit: int) -> NewAlbumsResponse:
        if limit <= 0:
            return exceptions.InvalidLimitParamException()

        usecase = container.resolve(GetNewAlbumsUseCase)
        output = await usecase.execute(GetNewAlbumsDto(limit=limit))
        return map_to_new_albums_success(output)

    @strawberry.field
    async def get_artists(self, page: int) -> ArtistsResponse:
        if page <= 0:
            return exceptions.InvalidPageParamException()

        usecase = container.resolve(GetArtistsUseCase)
        output = await usecase.execute(GetArtistsDto(page=page))
        return map_to_artists_success(output)
