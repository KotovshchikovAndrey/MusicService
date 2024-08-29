from domain.common.exceptions import NotFoundException
from domain.common.mappers import map_to_artist_dto
from domain.dtos.inputs import UpdateArtistDto
from domain.dtos.outputs import ArtistDto
from domain.usecases.base import BaseUseCase
from domain.utils.uow import UnitOfWork


class UpdateArtistUseCase(BaseUseCase[UpdateArtistDto, ArtistDto]):
    _uow: UnitOfWork

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, data: UpdateArtistDto) -> ArtistDto:
        async with self._uow as uow:
            artist = await uow.artists.get_by_id(data.id)
            if artist is None:
                raise NotFoundException()

            if data.nickname is not None:
                artist.change_nickname(data.nickname)

            if data.avatar_url is not None:
                artist.change_avatar(data.avatar_url)

            await uow.artists.save(artist)
            await uow.commit()

        return map_to_artist_dto(artist)
