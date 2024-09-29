from adapters.driving.graphql.schemas.artist import (
    ArtistSchema,
    BaseArtistSchema,
    PaginatedArtistListSchema,
)
from domain.models.entities.artist import Artist, BaseArtist
from domain.ports.driving.artist_list_getting import PaginatedArtistList


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


def map_to_paginated_artist_list_schema(
    data: PaginatedArtistList,
) -> PaginatedArtistListSchema:
    return PaginatedArtistListSchema(
        count=data.count,
        total_count=data.total_count,
        total_pages=data.total_pages,
        current_page=data.current_page,
        prev_page=data.prev_page,
        next_page=data.next_page,
        artists=[map_to_artist_schema(artist) for artist in data.artists],
    )
