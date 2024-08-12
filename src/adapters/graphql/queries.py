from typing import Any

import strawberry

from adapters.graphql.context import GraphqlContext
from adapters.graphql.schemas.mappers import (
    map_to_album_info_schema,
    map_to_charted_track_schema,
)
from adapters.graphql.schemas.responses import ChartResponse, NewReleasesResponse
from domain.dtos.inputs import GetChartDto, GetNewReleasesDto


@strawberry.type
class Query:
    @strawberry.field
    async def chart(
        self, limit: int, info: strawberry.Info[GraphqlContext, Any]
    ) -> ChartResponse:
        if limit <= 0:
            return ChartResponse(
                status_code=400,
                message="Invalid limit param",
                tracks=[],
            )

        usecase = info.context.get_chart_usecase
        tracks = await usecase.execute(GetChartDto(limit=limit))
        return ChartResponse(
            tracks=[map_to_charted_track_schema(track) for track in tracks]
        )

    @strawberry.field
    async def new_releases(
        self, limit: int, info: strawberry.Info[GraphqlContext, Any]
    ) -> NewReleasesResponse:
        if limit <= 0:
            return NewReleasesResponse(
                message="Invalid limit param",
                status_code=400,
                albums=[],
            )

        usecase = info.context.get_new_releases
        albums = await usecase.execute(GetNewReleasesDto(limit=limit))
        return NewReleasesResponse(
            albums=[map_to_album_info_schema(album) for album in albums]
        )
