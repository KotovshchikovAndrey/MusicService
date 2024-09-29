from domain.exceptions.base import InvalidInput


class InvalidAlbumInput(InvalidInput):
    def __init__(self, detail: str) -> None:
        super().__init__(detail=detail)
