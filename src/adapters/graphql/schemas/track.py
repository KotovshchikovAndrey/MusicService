import strawberry

from adapters.graphql.schemas.artist import ArtistSchema


@strawberry.type
class TrackSchema:
    oid: strawberry.ID
    album_oid: str
    title: str
    audio_url: str
    duration: str
    listens: int
    cover_url: str
    artists: tuple[ArtistSchema]
