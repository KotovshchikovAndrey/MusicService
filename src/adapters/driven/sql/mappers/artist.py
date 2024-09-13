from adapters.driven.sql.models.artist import Artist as ArtistModel
from domain.models.entities.artist import Artist, BaseArtist
from domain.models.values.avatar_url import AvatarUrl
from domain.models.values.nickname import Nickname


def map_to_base_artist(artist_model: ArtistModel) -> BaseArtist:
    base_artist = BaseArtist(id=artist_model.id)
    base_artist.nickname = Nickname(artist_model.nickname)

    return base_artist


def map_to_artist(artist_model: ArtistModel) -> Artist:
    artist = Artist(id=artist_model.id)
    artist.nickname = Nickname(artist_model.nickname)
    artist.avatar_url = AvatarUrl(artist_model.avatar_url)

    return artist


def map_to_artist_model(artist: Artist) -> ArtistModel:
    artist_model = ArtistModel(id=artist.id)
    artist_model.nickname = artist.nickname.value
    artist_model.avatar_url = artist.avatar_url.value

    return artist_model
