from adapters.driven.sql.mappers.artist import map_to_base_artist
from adapters.driven.sql.models.track import Track as TrackModel
from domain.models.entities.track import PopularTrack, Track, TrackItem
from domain.models.values.audio_url import AudioUrl
from domain.models.values.cover_url import CoverUrl
from domain.models.values.duration import Duration
from domain.models.values.listens import Listens
from domain.models.values.title import Title


def map_to_track(track_model: TrackModel) -> Track:
    return Track(
        id=track_model.id,
        album_id=track_model.album_id,
        title=Title(track_model.title),
        audio_url=AudioUrl(track_model.audio_url),
        duration=Duration(track_model.duration),
    )


def map_to_track_item(track_model: TrackModel) -> TrackItem:
    return TrackItem(
        id=track_model.id,
        album_id=track_model.album_id,
        title=Title(track_model.title),
        audio_url=AudioUrl(track_model.audio_url),
        duration=Duration(track_model.duration),
        listens=Listens(track_model.listens),
        artists=tuple(map_to_base_artist(model) for model in track_model.artists),
    )


def map_to_popular_track(track_model: TrackModel) -> PopularTrack:
    return PopularTrack(
        id=track_model.id,
        album_id=track_model.album_id,
        title=Title(track_model.title),
        audio_url=AudioUrl(track_model.audio_url),
        duration=Duration(track_model.duration),
        cover_url=CoverUrl(track_model.album.cover_url),
        listens=Listens(track_model.listens),
        artists=tuple(map_to_base_artist(model) for model in track_model.artists),
    )


def map_to_insert_track_values(track: Track) -> dict:
    return {
        "id": track.id,
        "title": track.title.value,
        "audio_url": track.audio_url.value,
        "duration": track.duration.value,
        "album_id": track.album_id,
    }
