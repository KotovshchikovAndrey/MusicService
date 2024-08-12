from datetime import UTC

from adapters.sql.mappers.track import map_to_track_item
from adapters.sql.models.album import AlbumModel
from domain.entities.album import Album, AlbumInfo
from domain.values.cover_url import CoverUrl
from domain.values.oid import OID
from domain.values.title import Title


def map_to_album(album_model: AlbumModel) -> Album:
    return Album(
        oid=OID(album_model.oid),
        title=Title(album_model.title),
        cover_url=CoverUrl(album_model.cover_url),
        created_at=album_model.created_at.replace(tzinfo=UTC),
    )


def map_to_album_info(album_model: AlbumModel) -> AlbumInfo:
    return AlbumInfo(
        oid=OID(album_model.oid),
        title=Title(album_model.title),
        cover_url=CoverUrl(album_model.cover_url),
        created_at=album_model.created_at.replace(tzinfo=UTC),
        tracks=tuple(map_to_track_item(model) for model in album_model.tracks),
    )


def map_to_album_model(album: Album) -> AlbumModel:
    return AlbumModel(
        oid=album.oid.value,
        title=album.title.value,
        cover_url=album.cover_url.value,
        created_at=album.created_at.replace(tzinfo=None),
    )
