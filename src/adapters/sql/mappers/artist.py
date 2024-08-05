from adapters.sql.models.artist import ArtistModel
from domain.entities.artist import Artist
from domain.values.avatar_url import AvatarUrl
from domain.values.nickname import Nickname
from domain.values.oid import OID


def map_to_artist_entity(artist_model: ArtistModel) -> Artist:
    return Artist(
        oid=OID(artist_model.oid),
        nickname=Nickname(artist_model.nickname),
        avatar_url=AvatarUrl(artist_model.avatar_url),
    )


def map_to_artist_model(artist: Artist) -> ArtistModel:
    return ArtistModel(
        oid=artist.oid.value,
        nickname=artist.nickname.value,
        avatar_url=artist.avatar_url.value,
    )
