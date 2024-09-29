from domain.exceptions.base import NotFound


class ArtistNotFound(NotFound):
    def __init__(self) -> None:
        super().__init__(detail="Artist not found")
