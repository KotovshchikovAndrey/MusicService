from typing import Annotated

import strawberry

from adapters.driving.graphql.schemas.exceptions import (
    InvalidLimitParamException,
    InvalidPageParamException,
)


@strawberry.type
class ArtistLinkSchema:
    id: strawberry.ID
    nickname: str


@strawberry.type
class ArtistSchema(ArtistLinkSchema):
    avatar_url: str


@strawberry.type
class TrackSchema:
    id: strawberry.ID
    title: str
    audio_url: str
    duration: str


@strawberry.type
class TrackItemSchema(TrackSchema):
    artists: tuple[ArtistLinkSchema]


@strawberry.type
class ChartedTrackSchema(TrackItemSchema):
    cover_url: str


@strawberry.type
class AlbumSchema:
    id: strawberry.ID
    title: str
    cover_url: str
    created_at: str


@strawberry.type
class AlbumInfoSchema(AlbumSchema):
    track: list[TrackItemSchema]


@strawberry.type
class PaginationSchema:
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
class NewReleasesSuccess:
    albums: list[AlbumInfoSchema]


@strawberry.type
class ArtistsSuccess:
    artists: list[ArtistSchema]
    pagination: PaginationSchema


ChartResponse = Annotated[
    ChartSuccess | InvalidLimitParamException,
    strawberry.union("ChartResponse"),
]

NewReleasesResponse = Annotated[
    NewReleasesSuccess | InvalidLimitParamException,
    strawberry.union("NewReleasesResponse"),
]

ArtistsResponse = Annotated[
    ArtistsSuccess | InvalidPageParamException,
    strawberry.union("ArtistsResponse"),
]
