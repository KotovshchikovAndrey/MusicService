from adapters.graphql.schemas.responses import (
    AlbumInfoSchema,
    ArtistLinkSchema,
    ChartedTrackSchema,
    TrackItemSchema,
)
from domain.dtos.outputs import (
    AlbumInfoDto,
    ArtistLinkDto,
    ChartedTrackDto,
    TrackItemDto,
)


def map_to_artist_link_schema(artist: ArtistLinkDto) -> ArtistLinkSchema:
    return ArtistLinkSchema(
        oid=artist.oid,
        nickname=artist.nickname,
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
