from datetime import UTC

from adapters.driven.sql.mappers.track import map_to_track_item
from adapters.driven.sql.models.album import Album as AlbumModel
from domain.models.entities.album import Album, AlbumInfo
from domain.models.values.cover_url import CoverUrl
from domain.models.values.title import Title


def map_to_album(album_model: AlbumModel) -> Album:
    return Album(
        id=album_model.id,
        title=Title(album_model.title),
        cover_url=CoverUrl(album_model.cover_url),
        created_at=album_model.created_at.replace(tzinfo=UTC),
    )


def map_to_album_info(album_model: AlbumModel) -> AlbumInfo:
    return AlbumInfo(
        id=album_model.id,
        title=Title(album_model.title),
        cover_url=CoverUrl(album_model.cover_url),
        tracks=tuple(map_to_track_item(model) for model in album_model.tracks),
        created_at=album_model.created_at.replace(tzinfo=UTC),
    )


def map_to_insert_album_values(album: Album) -> dict:
    return {
        "id": album.id,
        "title": album.title.value,
        "cover_url": album.cover_url.value,
        "created_at": album.created_at.replace(tzinfo=None),
    }
