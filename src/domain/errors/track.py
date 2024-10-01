from domain.errors.base import NotFoundError


class TrackNotFoundError(NotFoundError):
    def __init__(self) -> None:
        super().__init__(message="Track not found")
