import strawberry

from adapters.driving.graphql.schemas.track import TrackItemSchema


@strawberry.type(name="Album")
class AlbumSchema:
    id: strawberry.ID
    title: str
    cover_url: str
    created_at: str


@strawberry.type(name="AlbumInfo")
class AlbumInfoSchema(AlbumSchema):
    track: list[TrackItemSchema]
