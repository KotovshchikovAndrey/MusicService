from domain.dtos.track import TrackDto
from domain.entities.track import Track
from domain.mappers.atrist import map_to_artist_dto


def map_to_track_dto(track: Track) -> TrackDto:
    return TrackDto(
        oid=track.oid,
        title=track.title.value,
        audio_url=track.audio_url.value,
        duration=track.duration.value,
        artists=[map_to_artist_dto(artist) for artist in track.artists],
    )
