from typing import Any

import strawberry

from adapters.graphql.context import GraphqlContext
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
from domain.dtos.inputs import GetArtistsDto, GetChartDto, GetNewReleasesDto


@strawberry.type
class Query:
    @strawberry.field
    async def chart(
        self, limit: int, info: strawberry.Info[GraphqlContext, Any]
    ) -> ChartResponse:
        if limit <= 0:
            return InvalidLimitParamException()

        usecase = info.context.get_chart
        tracks = await usecase.execute(GetChartDto(limit=limit))
        return ChartSuccess(
            tracks=[map_to_charted_track_schema(track) for track in tracks]
        )

    @strawberry.field
    async def new_releases(
        self, limit: int, info: strawberry.Info[GraphqlContext, Any]
    ) -> NewReleasesResponse:
        if limit <= 0:
            return InvalidLimitParamException()

        usecase = info.context.get_new_releases
        albums = await usecase.execute(GetNewReleasesDto(limit=limit))
        return NewReleasesSuccess(
            albums=[map_to_album_info_schema(album) for album in albums]
        )

    @strawberry.field
    async def artists(
        self, page: int, info: strawberry.Info[GraphqlContext, Any]
    ) -> ArtistsResponse:
        if page <= 0:
            return InvalidPageParamException()

        usecase = info.context.get_artists
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
