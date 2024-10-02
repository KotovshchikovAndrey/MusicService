import strawberry

from adapters.driving.graphql.mappers.album import map_to_album_info_schema
from adapters.driving.graphql.mappers.artist import map_to_paginated_artists_schema
from adapters.driving.graphql.mappers.track import (
    map_to_popular_track_schema,
    map_to_track_item_schema,
)
from adapters.driving.graphql.permissions import IsAuthenticated
from adapters.driving.graphql.resolvers.inputs import SearchTrackInput
from adapters.driving.graphql.schemas.album import AlbumInfoSchema
from adapters.driving.graphql.schemas.artist import PaginatedArtistsSchema
from adapters.driving.graphql.schemas.track import PopularTrackSchema, TrackItemSchema
from config.ioc_container import container
from domain.ports.driving.albums_getting import GetAlbumsDTO, GetAlbumsUseCase
from domain.ports.driving.artists_getting import (
    GetArtistsDTO,
    GetArtistsUseCase,
)
from domain.ports.driving.chart_getting import GetChartDTO, GetChartUseCase
from domain.ports.driving.track_search import SearchTrackUseCase


@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def get_chart(self, limit: int) -> list[PopularTrackSchema]:
        usecase = container.resolve(GetChartUseCase)
        tracks = await usecase.execute(GetChartDTO(limit=limit))
        return [map_to_popular_track_schema(track) for track in tracks]

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def get_albums(self, limit: int) -> list[AlbumInfoSchema]:
        usecase = container.resolve(GetAlbumsUseCase)
        albums = await usecase.execute(GetAlbumsDTO(limit=limit))
        return [map_to_album_info_schema(album) for album in albums]

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def get_artists(self, page: int) -> PaginatedArtistsSchema:
        usecase = container.resolve(GetArtistsUseCase)
        artists = await usecase.execute(GetArtistsDTO(page=page))
        return map_to_paginated_artists_schema(artists)

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def search_track(self, input_query: SearchTrackInput) -> list[TrackItemSchema]:
        usecase = container.resolve(SearchTrackUseCase)
        tracks = await usecase.execute(input_query.to_dto())
        return [map_to_track_item_schema(track) for track in tracks]
