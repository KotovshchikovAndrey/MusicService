from domain.exceptions.base import NotFound


class TrackNotFound(NotFound):
    def __init__(self) -> None:
        super().__init__(detail="Track not found")
