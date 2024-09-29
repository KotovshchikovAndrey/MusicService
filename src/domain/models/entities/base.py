from abc import ABC
from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(eq=False, slots=True, kw_only=True)
class BaseEntity(ABC):
    id: UUID = field(default_factory=uuid4)

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, BaseEntity):
            return False

        return self.id == value.id
