from dataclasses import dataclass
import enum


class ExcCode(enum.IntEnum):
    BAD_REQUEST = 400
    NOT_FOUND = 404
    CONFLICT = 409


@dataclass(eq=False, slots=True)
class BaseDomainException(Exception):
    @property
    def code(self) -> ExcCode: ...

    @property
    def detail(self) -> str: ...
