import strawberry


@strawberry.type
class ArtistLinkSchema:
    oid: strawberry.ID
    nickname: str


@strawberry.type
class ArtistSchema(ArtistLinkSchema):
    avatar_url: str


@strawberry.type
class TrackItemSchema:
    oid: strawberry.ID
    title: str
    audio_url: str
    duration: str
    artists: tuple[ArtistLinkSchema]


@strawberry.type
class ChartedTrackSchema(TrackItemSchema):
    cover_url: str


@strawberry.type
class AlbumInfoSchema:
    oid: strawberry.ID
    title: str
    cover_url: str
    created_at: str
    track: list[TrackItemSchema]
