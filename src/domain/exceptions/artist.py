from domain.exceptions.base import BaseDomainException, ExcCode


class ArtistNotFound(BaseDomainException):
    @property
    def code(self) -> ExcCode:
        return ExcCode.NOT_FOUND

    @property
    def detail(self) -> str:
        return "Artist not found"


class ArtistExists(BaseDomainException):
    @property
    def code(self) -> ExcCode:
        return ExcCode.CONFLICT

    @property
    def detail(self) -> str:
        return "Artist already exists"
