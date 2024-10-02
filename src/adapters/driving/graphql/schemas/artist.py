import strawberry

from adapters.driving.graphql.schemas.base import PaginationSchema


@strawberry.type(name="BaseArtist")
class BaseArtistSchema:
    id: strawberry.ID
    nickname: str


@strawberry.type(name="Artist")
class ArtistSchema(BaseArtistSchema):
    avatar_url: str


@strawberry.type(name="PaginatedArtists")
class PaginatedArtistsSchema(PaginationSchema):
    artists: list[ArtistSchema]
