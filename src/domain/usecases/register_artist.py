from domain.common import consts
from domain.common.exceptions import ConflictException
from domain.dtos.inputs import RegisterArtistDto
from domain.factories.artist import ArtistFactory
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

        artist_factory = ArtistFactory(
            user_oid=data.oid,
            nickname=data.nickname,
            avatar_url=consts.DEFAULT_ARTIST_AVATAR,
        )

        artist = artist_factory.create()
        async with self._uow as uow:
            await uow.artists.upsert(artist)
            await uow.commit()
