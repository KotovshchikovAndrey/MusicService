from domain.errors.base import InvalidInputError


class InvalidAlbumError(InvalidInputError):
    def __init__(self, message: str) -> None:
        super().__init__(message=message)
