from domain.common import consts
from domain.dtos.artist import RegisterArtistDto
from domain.entities.artist import Artist
from domain.exceptions.conflict import ConflictException
from domain.usecases.base import BaseUseCase
from domain.utils.uow import UnitOfWork


class RegisterArtistUseCase(BaseUseCase[RegisterArtistDto, None]):
    _uow: UnitOfWork

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, data: RegisterArtistDto) -> None:
        async with self._uow as uow:
            artist = await uow.artists.get_by_oid(data.oid)
            if artist is not None:
                raise ConflictException("Artist already exists")

        artist = Artist.create(
            oid=data.oid,
            nickname=data.nickname,
            avatar_url=consts.DEFAULT_ARTIST_AVATAR,
        )

        async with self._uow as uow:
            await uow.artists.upsert(artist)
            await uow.commit()
