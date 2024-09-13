from adapters.driving.graphql.models.schemas import (
    AlbumInfoSchema,
    ArtistSchema,
    BaseArtistSchema,
    ChartedTrackSchema,
    TrackItemSchema,
)
from domain.models.entities.album import AlbumInfo
from domain.models.entities.artist import Artist, BaseArtist
from domain.models.entities.track import ChartedTrack, TrackItem


def map_to_base_artist_schema(artist: BaseArtist) -> BaseArtistSchema:
    return BaseArtistSchema(
        id=artist.id,
        nickname=artist.nickname.value,
    )


def map_to_artist_schema(artist: Artist) -> BaseArtistSchema:
    return ArtistSchema(
        id=artist.id,
        nickname=artist.nickname.value,
        avatar_url=artist.avatar_url.value,
    )


def map_to_charted_track_schema(track: ChartedTrack) -> ChartedTrackSchema:
    return ChartedTrackSchema(
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


def map_to_album_info_schema(album: AlbumInfo) -> AlbumInfoSchema:
    return AlbumInfoSchema(
        id=album.id,
        title=album.title.value,
        created_at=album.created_at,
        cover_url=album.cover_url.value,
        track=[map_to_track_item_schema(track) for track in album.tracks],
    )
