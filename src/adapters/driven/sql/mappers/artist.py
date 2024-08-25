from adapters.driven.sql.models.artist import ArtistModel
from domain.entities.artist import Artist, ArtistLink
from domain.values.avatar_url import AvatarUrl
from domain.values.nickname import Nickname


def map_to_artist_link(artist_model: ArtistModel) -> ArtistLink:
    return ArtistLink(
        id=artist_model.id,
        nickname=Nickname(artist_model.nickname),
    )


def map_to_artist(artist_model: ArtistModel) -> Artist:
    return Artist(
        id=artist_model.id,
        nickname=Nickname(artist_model.nickname),
        avatar_url=AvatarUrl(artist_model.avatar_url),
    )


def map_to_artist_model(artist: Artist) -> ArtistModel:
    return ArtistModel(
        id=artist.id,
        nickname=artist.nickname.value,
        avatar_url=artist.avatar_url.value,
    )
