import typing as tp
import uuid
from dataclasses import dataclass

from domain.values.base import BaseValue


@dataclass(frozen=True, slots=True)
class OID(BaseValue[str]):
    def validate(self) -> None:
        try:
            uuid.UUID(self.value)
        except ValueError:
            raise ValueError("Invalid oid value. Excpected valid uuid4 string")

    @classmethod
    def generate(cls: tp.Type["OID"]) -> "OID":
        return cls(uuid.uuid4().hex)
