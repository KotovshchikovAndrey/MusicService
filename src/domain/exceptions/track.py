from domain.exceptions.base import BaseDomainException, ExcCode


class TrackNotFound(BaseDomainException):
    @property
    def code(self) -> ExcCode:
        return ExcCode.NOT_FOUND

    @property
    def detail(self) -> str:
        return "Track not found"
