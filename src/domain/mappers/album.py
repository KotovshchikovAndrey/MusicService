from domain.dtos.album import AlbumDto, AlbumWithTracksDto
from domain.entities.album import Album
from domain.mappers.track import map_to_track_dto


def map_to_album_dto(album: Album) -> AlbumDto:
    return AlbumDto(
        oid=album.oid.value,
        title=album.title.value,
        cover_url=album.cover_url.value,
        created_at=album.created_at,
    )


def map_to_album_with_tracks_dto(album: Album) -> AlbumWithTracksDto:
    return AlbumWithTracksDto(
        oid=album.oid.value,
        title=album.title.value,
        cover_url=album.cover_url.value,
        created_at=album.created_at,
        tracks=[map_to_track_dto(track) for track in album.tracks],
    )
