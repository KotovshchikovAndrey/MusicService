import strawberry
from adapters.graphql.mappers.artist import map_to_artist_schema
from adapters.graphql.schemas.track import TrackSchema
from domain.dtos.track import TrackDto


def map_to_track_schema(track: TrackDto) -> TrackSchema:
    return TrackSchema(
        oid=strawberry.ID(track.oid),
        title=track.oid,
        audio_url=track.audio_url,
        duration=track.duration,
        listens=track.listens,
        album_oid=track.album_oid,
        cover_url=track.cover_url,
        artists=[map_to_artist_schema(artist) for artist in track.artists],
    )
