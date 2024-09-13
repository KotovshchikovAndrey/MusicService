from datetime import UTC

from adapters.driven.sql.mappers.track import map_to_track_item
from adapters.driven.sql.models.album import Album as AlbumModel
from domain.models.entities.album import Album, AlbumInfo
from domain.models.values.cover_url import CoverUrl
from domain.models.values.title import Title


def map_to_album(album_model: AlbumModel) -> Album:
    album = Album(id=album_model.id)
    album.title = Title(album_model.title)
    album.cover_url = CoverUrl(album_model.cover_url)
    album.created_at = album_model.created_at.replace(tzinfo=UTC)

    return album


def map_to_album_info(album_model: AlbumModel) -> AlbumInfo:
    album_info = AlbumInfo(id=album_model.id)
    album_info.title = Title(album_model.title)
    album_info.cover_url = CoverUrl(album_model.cover_url)
    album_info.created_at = album_model.created_at.replace(tzinfo=UTC)
    album_info.tracks = tuple(map_to_track_item(model) for model in album_model.tracks)

    return album_info


def map_to_album_model(album: Album) -> AlbumModel:
    album_model = AlbumModel(id=album.id)
    album_model.title = album.title.value
    album_model.cover_url = album.cover_url.value
    album_model.created_at = album.created_at.replace(tzinfo=None)

    return album_model
