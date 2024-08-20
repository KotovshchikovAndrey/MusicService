from adapters.sql.mappers.artist import map_to_artist_link
from adapters.sql.models.track import TrackModel
from domain.entities.track import ChartedTrack, Track, TrackItem
from domain.values.audio_url import AudioUrl
from domain.values.cover_url import CoverUrl
from domain.values.duration import Duration
from domain.values.listens import Listens
from domain.values.title import Title


def map_to_track(track_model: TrackModel) -> Track:
    return Track(
        id=track_model.id,
        album_id=track_model.album_id,
        title=Title(track_model.title),
        audio_url=AudioUrl(track_model.audio_url),
        duration=Duration(track_model.duration),
        listens=Listens(track_model.listens),
    )


def map_to_track_item(track_model: TrackModel) -> TrackItem:
    return TrackItem(
        id=track_model.id,
        album_id=track_model.album_id,
        title=Title(track_model.title),
        audio_url=AudioUrl(track_model.audio_url),
        duration=Duration(track_model.duration),
        listens=Listens(track_model.listens),
        artists=tuple(map_to_artist_link(model) for model in track_model.artists),
    )


def map_to_charted_track(track_model: TrackModel) -> ChartedTrack:
    return ChartedTrack(
        id=track_model.id,
        album_id=track_model.album_id,
        title=Title(track_model.title),
        audio_url=AudioUrl(track_model.audio_url),
        duration=Duration(track_model.duration),
        cover_url=CoverUrl(track_model.album.cover_url),
        listens=Listens(track_model.listens),
        artists=tuple(map_to_artist_link(model) for model in track_model.artists),
    )


def map_to_track_model(track: Track) -> TrackModel:
    return TrackModel(
        id=track.id,
        title=track.title.value,
        audio_url=track.audio_url.value,
        duration=track.duration.value,
        album_id=track.album_id,
    )
