from typing import Iterable

from adapters.driving.graphql.mappers.schemas import (
    map_to_album_info_schema,
    map_to_artist_schema,
    map_to_charted_track_schema,
)
from adapters.driving.graphql.models.responses import (
    ArtistsSuccess,
    ChartSuccess,
    NewAlbumsSuccess,
)
from domain.models.entities.album import AlbumInfo
from domain.models.entities.track import ChartedTrack
from domain.ports.driving.getting_artists import PaginatedArtists


def map_to_chart_success(data: Iterable[ChartedTrack]) -> ChartSuccess:
    return ChartSuccess(tracks=[map_to_charted_track_schema(track) for track in data])


def map_to_new_albums_success(data: Iterable[AlbumInfo]) -> NewAlbumsSuccess:
    return NewAlbumsSuccess(albums=[map_to_album_info_schema(album) for album in data])


def map_to_artists_success(data: PaginatedArtists) -> ArtistsSuccess:
    return ArtistsSuccess(
        count=data.count,
        total_count=data.total_count,
        total_pages=data.total_pages,
        current_page=data.current_page,
        prev_page=data.prev_page,
        next_page=data.next_page,
        artists=[map_to_artist_schema(artist) for artist in data.artists],
    )
