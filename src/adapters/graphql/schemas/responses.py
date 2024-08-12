import strawberry


@strawberry.type
class ArtistLinkSchema:
    oid: strawberry.ID
    nickname: str


@strawberry.type
class ArtistSchema(ArtistLinkSchema):
    avatar_url: str


@strawberry.type
class TrackSchema:
    oid: strawberry.ID
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
    oid: strawberry.ID
    title: str
    cover_url: str
    created_at: str


@strawberry.type
class AlbumInfoSchema(AlbumSchema):
    track: list[TrackItemSchema]


@strawberry.type
class ApiResponse:
    status_code: int = 200
    message: str = "Success"


@strawberry.type
class ChartResponse(ApiResponse):
    tracks: list[ChartedTrackSchema]


@strawberry.type
class NewReleasesResponse(ApiResponse):
    albums: list[AlbumInfoSchema]
