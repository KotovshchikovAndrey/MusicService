from dataclasses import dataclass

from domain.values.base import Url


@dataclass(frozen=True, slots=True)
class CoverUrl(Url):
    def get_pattern(self) -> str:
        return r"\/[a-zA-Z\d\-_]+\.(png|jpeg|jpg)"
