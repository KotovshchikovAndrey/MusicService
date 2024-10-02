from adapters.driving.graphql.schemas.artist import (
    ArtistSchema,
    BaseArtistSchema,
    PaginatedArtistsSchema,
)
from domain.models.entities.artist import Artist, BaseArtist
from domain.ports.driving.artists_getting import PaginatedArtists


def map_to_base_artist_schema(artist: BaseArtist) -> BaseArtistSchema:
    return BaseArtistSchema(
        id=artist.id,
        nickname=artist.nickname.value,
    )


def map_to_artist_schema(artist: Artist) -> ArtistSchema:
    return ArtistSchema(
        id=artist.id,
        nickname=artist.nickname.value,
        avatar_url=artist.avatar_url.value,
    )


def map_to_paginated_artists_schema(
    data: PaginatedArtists,
) -> PaginatedArtistsSchema:
    return PaginatedArtistsSchema(
        count=data.count,
        total_count=data.total_count,
        total_pages=data.total_pages,
        current_page=data.current_page,
        prev_page=data.prev_page,
        next_page=data.next_page,
        artists=[map_to_artist_schema(artist) for artist in data.artists],
    )
