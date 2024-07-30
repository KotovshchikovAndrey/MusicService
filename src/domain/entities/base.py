import uuid
from abc import ABC
from dataclasses import dataclass, field


@dataclass(eq=False, kw_only=True, slots=True)
class BaseEntity(ABC):
    oid: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, BaseEntity):
            return False

        return self.oid == value.oid
