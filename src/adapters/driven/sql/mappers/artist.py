from adapters.driven.sql.models.artist import Artist as ArtistModel
from domain.models.entities.artist import Artist, BaseArtist
from domain.models.values.avatar_url import AvatarUrl
from domain.models.values.nickname import Nickname


def map_to_base_artist(artist_model: ArtistModel) -> BaseArtist:
    return BaseArtist(
        id=artist_model.id,
        nickname=Nickname(artist_model.nickname),
    )


def map_to_artist(artist_model: ArtistModel) -> Artist:
    return Artist(
        id=artist_model.id,
        nickname=Nickname(artist_model.nickname),
        avatar_url=AvatarUrl(artist_model.avatar_url),
    )


def map_to_insert_artist_values(artist: Artist) -> dict:
    return {
        "id": artist.id,
        "nickname": artist.nickname.value,
        "avatar_url": artist.avatar_url.value,
    }
