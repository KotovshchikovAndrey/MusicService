from typing import Any
import strawberry

from adapters.graphql.context import GraphqlContext
from adapters.graphql.mappers.album import map_to_album_schema
from adapters.graphql.mappers.track import map_to_track_schema
from adapters.graphql.schemas.album import AlbumSchema
from adapters.graphql.schemas.track import TrackSchema
from domain.dtos.album import GetNewReleasesDto
from domain.dtos.track import GetChartDto


@strawberry.type
class Query:
    @strawberry.field
    async def chart(
        self, info: strawberry.Info[GraphqlContext, Any]
    ) -> list[TrackSchema]:
        usecase = info.context.get_chart_usecase
        tracks = await usecase.execute(GetChartDto(limit=100))
        return [map_to_track_schema(track) for track in tracks]

    @strawberry.field
    async def new_releases(
        self, info: strawberry.Info[GraphqlContext, Any]
    ) -> list[AlbumSchema]:
        usecase = info.context.get_new_releases
        albums = await usecase.execute(GetNewReleasesDto(limit=100))
        return [map_to_album_schema(album) for album in albums]
