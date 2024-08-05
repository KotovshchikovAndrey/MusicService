from dataclasses import dataclass

from domain.values.base import Url


@dataclass(frozen=True, slots=True)
class AudioUrl(Url):
    def get_pattern(self) -> str:
        return r"\/[a-zA-Z\d\-_]+\.(aac|mp3|flac)"
