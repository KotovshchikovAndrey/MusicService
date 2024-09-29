from adapters.driving.graphql.mappers.track import map_to_track_item_schema
from adapters.driving.graphql.schemas.album import AlbumInfoSchema
from domain.models.entities.album import AlbumInfo


def map_to_album_info_schema(album: AlbumInfo) -> AlbumInfoSchema:
    return AlbumInfoSchema(
        id=album.id,
        title=album.title.value,
        created_at=album.created_at,
        cover_url=album.cover_url.value,
        track=[map_to_track_item_schema(track) for track in album.tracks],
    )
