import strawberry


@strawberry.type
class BaseArtistSchema:
    id: strawberry.ID
    nickname: str


@strawberry.type
class ArtistSchema(BaseArtistSchema):
    avatar_url: str


@strawberry.type
class TrackSchema:
    id: strawberry.ID
    title: str
    audio_url: str
    duration: str


@strawberry.type
class TrackItemSchema(TrackSchema):
    artists: tuple[BaseArtistSchema]


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
