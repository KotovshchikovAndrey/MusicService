from adapters.sql.mappers.artist import map_to_artist_link
from adapters.sql.models.track import TrackModel
from domain.entities.track import ChartedTrack, Track, TrackItem
from domain.values.audio_url import AudioUrl
from domain.values.cover_url import CoverUrl
from domain.values.duration import Duration
from domain.values.listens import Listens
from domain.values.oid import OID
from domain.values.title import Title


def map_to_track(track_model: TrackModel) -> Track:
    return Track(
        oid=OID(track_model.oid),
        album_oid=OID(track_model.album_oid),
        title=Title(track_model.title),
        audio_url=AudioUrl(track_model.audio_url),
        duration=Duration(track_model.duration),
        listens=Listens(track_model.listens),
    )


def map_to_track_item(track_model: TrackModel) -> TrackItem:
    return TrackItem(
        oid=OID(track_model.oid),
        album_oid=OID(track_model.album_oid),
        title=Title(track_model.title),
        audio_url=AudioUrl(track_model.audio_url),
        duration=Duration(track_model.duration),
        listens=Listens(track_model.listens),
        artists=tuple(map_to_artist_link(model) for model in track_model.artists),
    )


def map_to_charted_track(track_model: TrackModel) -> ChartedTrack:
    return ChartedTrack(
        oid=OID(track_model.oid),
        album_oid=OID(track_model.album_oid),
        title=Title(track_model.title),
        audio_url=AudioUrl(track_model.audio_url),
        duration=Duration(track_model.duration),
        cover_url=CoverUrl(track_model.album.cover_url),
        listens=Listens(track_model.listens),
        artists=tuple(map_to_artist_link(model) for model in track_model.artists),
    )


def map_to_track_model(track: Track) -> TrackModel:
    return TrackModel(
        oid=track.oid.value,
        title=track.title.value,
        audio_url=track.audio_url.value,
        duration=track.duration.value,
    )
