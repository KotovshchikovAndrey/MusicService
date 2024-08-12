from adapters.graphql.schemas.responses import (
    AlbumInfoSchema,
    ArtistLinkSchema,
    ArtistSchema,
    ChartedTrackSchema,
    TrackItemSchema,
)
from domain.dtos.outputs import (
    AlbumInfoDto,
    ArtistDto,
    ArtistLinkDto,
    ChartedTrackDto,
    TrackItemDto,
)


def map_to_artist_link_schema(artist: ArtistLinkDto) -> ArtistLinkSchema:
    return ArtistLinkSchema(
        oid=artist.oid,
        nickname=artist.nickname,
    )


def map_to_artist_schema(artist: ArtistDto) -> ArtistLinkSchema:
    return ArtistSchema(
        oid=artist.oid,
        nickname=artist.nickname,
        avatar_url=artist.avatar_url,
    )


def map_to_charted_track_schema(track: ChartedTrackDto) -> ChartedTrackSchema:
    return ChartedTrackSchema(
        oid=track.oid,
        title=track.title,
        duration=track.duration,
        audio_url=track.audio_url,
        cover_url=track.cover_url,
        artists=[map_to_artist_link_schema(artist) for artist in track.artists],
    )


def map_to_track_item_schema(track: TrackItemDto) -> TrackItemSchema:
    return TrackItemSchema(
        oid=track.oid,
        title=track.title,
        audio_url=track.audio_url,
        duration=track.duration,
        artists=[map_to_artist_link_schema(artist) for artist in track.artists],
    )


def map_to_album_info_schema(album: AlbumInfoDto) -> AlbumInfoSchema:
    return AlbumInfoSchema(
        oid=album.oid,
        title=album.title,
        created_at=album.created_at,
        cover_url=album.cover_url,
        track=[map_to_track_item_schema(track) for track in album.tracks],
    )
