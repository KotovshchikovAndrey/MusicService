from dataclasses import dataclass
from domain.entities.base import BaseEntity

from domain.values.fullname import FullName


@dataclass(eq=False, kw_only=True, slots=True)
class Artist(BaseEntity):
    fullname: FullName

    def set_fullname(self, fullname: str) -> None:
        self.fullname = FullName(fullname)
