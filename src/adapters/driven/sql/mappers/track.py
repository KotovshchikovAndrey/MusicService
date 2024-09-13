from adapters.driven.sql.mappers.artist import map_to_base_artist
from adapters.driven.sql.models.track import Track as TrackModel
from domain.models.entities.track import ChartedTrack, Track, TrackItem
from domain.models.values.audio_url import AudioUrl
from domain.models.values.cover_url import CoverUrl
from domain.models.values.duration import Duration
from domain.models.values.listens import Listens
from domain.models.values.title import Title


def map_to_track(track_model: TrackModel) -> Track:
    track = Track(id=track_model.id)
    track.album_id = track_model.album_id
    track.title = Title(track_model.title)
    track.audio_url = AudioUrl(track_model.audio_url)
    track.duration = Duration(track_model.duration)
    track.listens = Listens(track_model.listens)

    return track


def map_to_track_item(track_model: TrackModel) -> TrackItem:
    track_item = TrackItem(id=track_model.id)
    track_item.album_id = track_model.album_id
    track_item.title = Title(track_model.title)
    track_item.audio_url = AudioUrl(track_model.audio_url)
    track_item.duration = Duration(track_model.duration)
    track_item.listens = Listens(track_model.listens)
    track_item.artists = tuple(map_to_base_artist(model) for model in track_model.artists)

    return track_item


def map_to_charted_track(track_model: TrackModel) -> ChartedTrack:
    charted_track = ChartedTrack(id=track_model.id)
    charted_track.album_id = track_model.album_id
    charted_track.title = Title(track_model.title)
    charted_track.audio_url = AudioUrl(track_model.audio_url)
    charted_track.duration = Duration(track_model.duration)
    charted_track.cover_url = CoverUrl(track_model.album.cover_url)
    charted_track.listens = Listens(track_model.listens)
    charted_track.artists = tuple(
        map_to_base_artist(model) for model in track_model.artists
    )

    return charted_track


def map_to_track_model(track: Track) -> TrackModel:
    track_model = TrackModel(id=track.id)
    track_model.title = track.title.value
    track_model.audio_url = track.audio_url.value
    track_model.duration = track.duration.value
    track_model.album_id = track.album_id

    return track_model
