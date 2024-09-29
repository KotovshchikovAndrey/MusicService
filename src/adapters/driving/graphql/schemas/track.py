import strawberry

from adapters.driving.graphql.schemas.artist import BaseArtistSchema


@strawberry.type(name="Track")
class TrackSchema:
    id: strawberry.ID
    title: str
    audio_url: str
    duration: str


@strawberry.type(name="TrackItem")
class TrackItemSchema(TrackSchema):
    artists: list[BaseArtistSchema]


@strawberry.type(name="PopularTrack")
class PopularTrackSchema(TrackItemSchema):
    cover_url: str
