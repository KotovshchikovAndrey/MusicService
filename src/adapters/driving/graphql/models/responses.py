from typing import Annotated

import strawberry

from adapters.driving.graphql.common import exceptions
from adapters.driving.graphql.models.schemas import (
    AlbumInfoSchema,
    ArtistSchema,
    ChartedTrackSchema,
)


@strawberry.type
class PaginationResponse:
    count: int
    total_count: int
    total_pages: int
    current_page: int
    next_page: int | None = None
    prev_page: int | None = None


@strawberry.type
class ChartSuccess:
    tracks: list[ChartedTrackSchema]


@strawberry.type
class NewAlbumsSuccess:
    albums: list[AlbumInfoSchema]


@strawberry.type
class ArtistsSuccess(PaginationResponse):
    artists: list[ArtistSchema]


ChartResponse = Annotated[
    ChartSuccess | exceptions.InvalidLimitParamException,
    strawberry.union("ChartResponse"),
]

NewAlbumsResponse = Annotated[
    NewAlbumsSuccess | exceptions.InvalidLimitParamException,
    strawberry.union("NewReleasesResponse"),
]

ArtistsResponse = Annotated[
    ArtistsSuccess | exceptions.InvalidPageParamException,
    strawberry.union("ArtistsResponse"),
]
