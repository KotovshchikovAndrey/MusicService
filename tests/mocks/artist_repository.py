from domain.entities.artist import Artist
from domain.repositories.artist import ArtistRepository


class MockedArtistRepository(ArtistRepository):
    _artists: dict[str, Artist]

    def __init__(self, artists: list[Artist]) -> None:
        self._artists = {artist.oid.value: artist for artist in artists}

    async def get_by_oid(self, artist_oid: str) -> Artist | None:
        return self._artists.get(artist_oid, None)

    async def filter_by_oids(self, *artist_oids: str) -> list[Artist]:
        artists = []
        for oid in artist_oids:
            artist = self._artists.get(oid, None)
            if artist is not None:
                artists.append(artist)

        return artists

    async def upsert(self, artist: Artist) -> None:
        self._artists[artist.oid.value] = artist
