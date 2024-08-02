from abc import ABC
from dataclasses import dataclass, field

from domain.values.oid import OID


@dataclass(eq=False, kw_only=True, slots=True)
class BaseEntity(ABC):
    oid: OID = field(default_factory=OID.generate)

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, BaseEntity):
            return False

        return self.oid == value.oid
