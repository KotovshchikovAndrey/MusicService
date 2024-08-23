import strawberry

from adapters.graphql.schemas.exceptions import (
    InvalidLimitParamException,
    InvalidPageParamException,
)
from adapters.graphql.schemas.mappers import (
    map_to_album_info_schema,
    map_to_artist_schema,
    map_to_charted_track_schema,
)
from adapters.graphql.schemas.responses import (
    ArtistsResponse,
    ArtistsSuccess,
    ChartResponse,
    ChartSuccess,
    NewReleasesResponse,
    NewReleasesSuccess,
    PaginationSchema,
)
from config.ioc_container import container
from domain.dtos.inputs import GetArtistsDto, GetChartDto, GetNewReleasesDto
from domain.usecases.get_artists import GetArtistsUseCase
from domain.usecases.get_chart import GetChartUseCase
from domain.usecases.get_new_releases import GetNewReleasesUseCase


@strawberry.type
class Query:
    @strawberry.field
    async def chart(self, limit: int) -> ChartResponse:
        if limit <= 0:
            return InvalidLimitParamException()

        usecase = container.resolve(GetChartUseCase)
        tracks = await usecase.execute(GetChartDto(limit=limit))
        return ChartSuccess(
            tracks=[map_to_charted_track_schema(track) for track in tracks]
        )

    @strawberry.field
    async def new_releases(self, limit: int) -> NewReleasesResponse:
        if limit <= 0:
            return InvalidLimitParamException()

        usecase = container.resolve(GetNewReleasesUseCase)
        albums = await usecase.execute(GetNewReleasesDto(limit=limit))
        return NewReleasesSuccess(
            albums=[map_to_album_info_schema(album) for album in albums]
        )

    @strawberry.field
    async def artists(self, page: int) -> ArtistsResponse:
        if page <= 0:
            return InvalidPageParamException()

        usecase = container.resolve(GetArtistsUseCase)
        output = await usecase.execute(GetArtistsDto(page=page))
        return ArtistsSuccess(
            artists=[map_to_artist_schema(artist) for artist in output.artists],
            pagination=PaginationSchema(
                count=output.count,
                total_count=output.total_count,
                total_pages=output.total_pages,
                current_page=output.current_page,
                prev_page=output.prev_page,
                next_page=output.next_page,
            ),
        )
