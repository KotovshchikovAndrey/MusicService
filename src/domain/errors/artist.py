from domain.errors.base import NotFoundError


class ArtistNotFoundError(NotFoundError):
    def __init__(self) -> None:
        super().__init__(message="Artist not found")
