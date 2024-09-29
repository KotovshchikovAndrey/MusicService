from adapters.driving.graphql.mappers.artist import map_to_base_artist_schema
from adapters.driving.graphql.schemas.track import PopularTrackSchema, TrackItemSchema
from domain.models.entities.track import PopularTrack, TrackItem


def map_to_popular_track_schema(track: PopularTrack) -> PopularTrackSchema:
    return PopularTrackSchema(
        id=track.id,
        title=track.title.value,
        duration=track.duration.value,
        audio_url=track.audio_url.value,
        cover_url=track.cover_url.value,
        artists=[map_to_base_artist_schema(artist) for artist in track.artists],
    )


def map_to_track_item_schema(track: TrackItem) -> TrackItemSchema:
    return TrackItemSchema(
        id=track.id,
        title=track.title.value,
        audio_url=track.audio_url.value,
        duration=track.duration.value,
        artists=[map_to_base_artist_schema(artist) for artist in track.artists],
    )
