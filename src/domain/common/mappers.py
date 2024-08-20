from domain.dtos.outputs import (
    AlbumInfoDto,
    ArtistDto,
    ArtistLinkDto,
    ChartedTrackDto,
    TrackItemDto,
)
from domain.entities.album import AlbumInfo
from domain.entities.artist import Artist
from domain.entities.track import ChartedTrack, TrackItem


def map_to_artist_link_dto(artist: Artist) -> ArtistDto:
    return ArtistLinkDto(
        id=artist.id,
        nickname=artist.nickname.value,
    )


def map_to_artist_dto(artist: Artist) -> ArtistDto:
    return ArtistDto(
        id=artist.id,
        nickname=artist.nickname.value,
        avatar_url=artist.avatar_url.value,
    )


def map_to_track_item_dto(track: TrackItem) -> TrackItemDto:
    return TrackItemDto(
        id=track.id,
        title=track.title.value,
        audio_url=track.audio_url.value,
        duration=track.duration.value,
        artists=[map_to_artist_link_dto(artist) for artist in track.artists],
    )


def map_to_album_info_dto(album: AlbumInfo) -> AlbumInfoDto:
    return AlbumInfoDto(
        id=album.id,
        title=album.title.value,
        cover_url=album.cover_url.value,
        created_at=album.created_at.isoformat(),
        tracks=[map_to_track_item_dto(track) for track in album.tracks],
    )


def map_to_charted_track_dto(track: ChartedTrack) -> ChartedTrackDto:
    return ChartedTrackDto(
        id=track.id,
        title=track.title.value,
        audio_url=track.audio_url.value,
        duration=track.duration.value,
        cover_url=track.cover_url.value,
        artists=[map_to_artist_link_dto(artist) for artist in track.artists],
    )
