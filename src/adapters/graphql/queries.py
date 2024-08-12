from typing import Any

import strawberry

from adapters.graphql.context import GraphqlContext
from adapters.graphql.schemas.mappers import (
    map_to_album_info_schema,
    map_to_charted_track_schema,
)
from adapters.graphql.schemas.responses import AlbumInfoSchema, ChartedTrackSchema
from domain.dtos.inputs import GetChartDto, GetNewReleasesDto


@strawberry.type
class Query:
    @strawberry.field
    async def chart(
        self, info: strawberry.Info[GraphqlContext, Any]
    ) -> list[ChartedTrackSchema]:
        usecase = info.context.get_chart_usecase
        tracks = await usecase.execute(GetChartDto(limit=100))
        return [map_to_charted_track_schema(track) for track in tracks]

    @strawberry.field
    async def new_releases(
        self, info: strawberry.Info[GraphqlContext, Any]
    ) -> list[AlbumInfoSchema]:
        usecase = info.context.get_new_releases
        albums = await usecase.execute(GetNewReleasesDto(limit=100))
        return [map_to_album_info_schema(album) for album in albums]
