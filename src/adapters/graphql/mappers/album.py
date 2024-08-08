import strawberry

from adapters.graphql.schemas.album import AlbumSchema
from domain.dtos.album import AlbumDto


def map_to_album_schema(album: AlbumDto) -> AlbumSchema:
    return AlbumSchema(
        oid=strawberry.ID(album.oid),
        title=album.title,
        cover_url=album.cover_url,
        created_at=album.created_at,
    )
