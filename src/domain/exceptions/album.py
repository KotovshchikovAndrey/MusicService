from dataclasses import dataclass
from domain.exceptions.base import BaseDomainException, ExcCode


@dataclass(eq=False, slots=True)
class InvalidAlbumUploadingData(BaseDomainException):
    reason: str

    @property
    def code(self) -> ExcCode:
        return ExcCode.BAD_REQUEST

    @property
    def detail(self) -> str:
        return f"Invalid album uploading data: {self.reason}"
