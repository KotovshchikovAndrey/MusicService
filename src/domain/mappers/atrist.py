from domain.dtos.artist import ArtistDto
from domain.entities.artist import Artist


def map_to_artist_dto(artist: Artist) -> ArtistDto:
    return ArtistDto(
        oid=artist.oid.value,
        nickname=artist.nickname.value,
    )
