from domain.exceptions.artist import ArtistNotFound
from domain.models.entities.artist import Artist
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driving.artist_updating import UpdateArtistDTO, UpdateArtistUseCase


class UpdateArtistUseCaseImpl(UpdateArtistUseCase):
    _uow: UnitOfWork

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, data: UpdateArtistDTO) -> Artist:
        async with self._uow as uow:
            artist = await uow.artists.get_by_id(data.artist_id)
            if artist is None:
                raise ArtistNotFound()

            if data.nickname is not None:
                artist.edit_nickname(data.nickname)

            if data.avatar_url is not None:
                artist.edit_avatar(data.avatar_url)

            await uow.artists.save(artist)
            await uow.commit()

        return artist
