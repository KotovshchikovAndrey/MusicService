import strawberry

from adapters.graphql.schemas.artist import ArtistSchema
from domain.dtos.artist import ArtistDto


def map_to_artist_schema(artist: ArtistDto) -> ArtistSchema:
    return ArtistSchema(
        oid=strawberry.ID(artist.oid),
        nickname=artist.nickname,
        avatar_url=artist.avatar_url,
    )
